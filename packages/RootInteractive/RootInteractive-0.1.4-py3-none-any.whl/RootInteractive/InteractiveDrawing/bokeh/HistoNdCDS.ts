import {ColumnarDataSource} from "models/sources/columnar_data_source"
import * as p from "core/properties"

export namespace HistoNdCDS {
  export type Attrs = p.AttrsOf<Props>

  export type Props = ColumnarDataSource.Props & {
    source: p.Property<ColumnarDataSource>
//    view: p.Property<number[] | null>
    nbins:        p.Property<number[]>
    range:    p.Property<(number[] | null)[] | null>
    sample_variables:      p.Property<string[]>
    weights:      p.Property<string | null>
    histograms: p.Property<Record<string, Record<string, any>>>
  }
}

export interface HistoNdCDS extends HistoNdCDS.Attrs {}

export class HistoNdCDS extends ColumnarDataSource {
  properties: HistoNdCDS.Props

  constructor(attrs?: Partial<HistoNdCDS.Attrs>) {
    super(attrs)

    this._range_min = []
    this._range_max = []
    this._transform_origin = []
    this._transform_scale = []
    this._strides = []
  }

  static __name__ = "HistoNdCDS"

  static init_HistoNdCDS() {

    this.define<HistoNdCDS.Props>(({Ref, Array, Nullable, Number, Int, String})=>({
      source:  [Ref(ColumnarDataSource)],
//      view:         [Nullable(Array(Int)), null], - specifying this as a bokeh property causes a drastic drop in performance
      nbins:        [Array(Int)],
      range:    [Nullable(Array(Nullable(Array(Number))))],
      sample_variables:      [Array(String)],
      weights:      [String, null],
      histograms:  [p.Instance]
    }))
  }

  initialize(): void {
    super.initialize()

    this.data = {"bin_count":[]}
    this.view = null
    this._bin_indices = []
    this.update_range()
  }

  connect_signals(): void {
    super.connect_signals()

    this.connect(this.source.change, () => {
      this._bin_indices.length = this.source.length
      this._bin_indices.fill(-2, 0, this.source.length)
      this.update_data()
    })
  }

  update_data(indices: number[] | null = null): void {
      let bincount = this.data["bin_count"] as number[]
      bincount.length = length
      if(indices != null){
        //TODO: Make this actually do something
      } else {
        bincount = this.histogram(this.weights)
        if(this.histograms !== null){
          for (const key in this.histograms){
            if(this.histograms[key] === null){
              this.data[key] = this.histogram(null)
            } else {
              this.data[key] = this.histogram(this.histograms[key].weights)
            }
          }
        }
      }
      this.data["bin_count"] = bincount
      this.data["errorbar_low"] = bincount.map(x=>x+Math.sqrt(x))
      this.data["errorbar_high"] = bincount.map(x=>x-Math.sqrt(x))
      this.change.emit()
  }

  public view: number[] | null

  public dim: number

  private _bin_indices: number[] // Bin index caching

  private _range_min: number[]
  private _range_max: number[]
  private _nbins: number[]
  private _transform_origin: number[]
  private _transform_scale: number[]
  private _strides: number[]

  update_range(): void {
    this._nbins = this.nbins;

    let sample_array: number[][] = []
    if(this.range === null || this.range.reduce((acc, cur) => acc || (cur === null), false))
    for (const column_name of this.sample_variables) {
      const column = this.source.get_array(column_name) as number[]
      sample_array.push(column)
    }
      // This code seems stupid
      let invalidate_bins = false
      if(this.view === null){
        if(this.range === null){
          for (let i = 0; i < this._nbins.length; i++) {
            this._range_min[i] = sample_array[i].reduce((acc, cur) => Math.min(acc, cur), Infinity)
            this._range_max[i] = sample_array[i].reduce((acc, cur) => Math.max(acc, cur), -Infinity)
          }
          invalidate_bins = true
        } else {
          for (let i = 0; i < this.range.length; i++) {
            const r = this.range[i]
            if(r === null) {
              this._range_min[i] = sample_array[i].reduce((acc, cur) => Math.min(acc, cur), Infinity)
              this._range_max[i] = sample_array[i].reduce((acc, cur) => Math.max(acc, cur), -Infinity)
              invalidate_bins = true
            } else {
              this._range_min[i] = r[0]
              this._range_max[i] = r[1]
            }
          }
        }
      } else {
        if(this.range === null){
          for (let i = 0; i < this._nbins.length; i++) {
            const col = sample_array[i]
            this._range_min[i] = this.view.reduce((acc, cur) => Math.min(acc, col[cur]), Infinity)
            this._range_max[i] = this.view.reduce((acc, cur) => Math.max(acc, col[cur]), -Infinity)
          }
          invalidate_bins = true
        } else {
          for (let i = 0; i < this.range.length; i++) {
            const r = this.range[i]
            if(r === null) {
              const col = sample_array[i]
              this._range_min[i] = this.view.reduce((acc, cur) => Math.min(acc, col[cur]), Infinity)
              this._range_max[i] = this.view.reduce((acc, cur) => Math.max(acc, col[cur]), -Infinity)
              invalidate_bins = true
            } else {
              this._range_min[i] = r[0]
              this._range_max[i] = r[1]
            }
          }
        }        
      }
      if (invalidate_bins || this._bin_indices.length === 0){
        this._bin_indices.length = this.source.length
        this._bin_indices.fill(-2, 0, this.source.length)
      }
      const dim = this.nbins.length
      this._nbins.length = dim
      this._transform_scale.length = dim
      this._transform_origin.length = dim
      this._strides.length = dim+1
      this._strides[0] = 1
      for(let i=0; i<dim; i++){
        this._nbins[i] = this.nbins[i]
        this._transform_scale[i] = this._nbins[i]/(this._range_max[i]-this._range_min[i])
        this._transform_origin[i] = this._range_min[i]*this._transform_scale[i]
        this._strides[i+1] = this._strides[i]*this._nbins[i]
      }

      const length = this._strides[dim]
      for(let i=0; i<dim; i++){
        let bin_bottom = []
        let bin_center = []
        let bin_top = []
        let inv_scale = 1/this._transform_scale[i]
        for (let index = 0; index < length; index++) {
          let true_index = ((index%this._strides[i+1])/this._strides[i])|0
          bin_bottom.push(this._range_min[i]+true_index*inv_scale)
          bin_center.push(this._range_min[i]+(true_index+.5)*inv_scale)
          bin_top.push(this._range_min[i]+(true_index+1)*inv_scale)
        }
        this.data["bin_bottom_"+i] = bin_bottom
        this.data["bin_center_"+i]  = bin_center
        this.data["bin_top_"+i]  = bin_top
      }

      this.dim = dim
      this.update_data()
  }

  histogram(weights: string | null): number[]{
    const length = this._strides[this._strides.length-1]
    let sample_array: number[][] = []
    for (const column_name of this.sample_variables) {
      sample_array.push(this.source.get_array(column_name))
    }
    let bincount: number[] = Array(length)
    bincount.fill(0)
    const view_indices = this.view
    if(view_indices === null){
      const n_indices = this.source.length
      if(weights != null){
        const weights_array = this.source.get_column(weights)
        if (weights_array == null){
          throw ReferenceError("Column not defined: "+ weights)
        }
        for(let i=0; i<n_indices; i++){
          const bin = this.getbin(i, sample_array)
          if(bin >= 0 && bin < length){
            bincount[bin] += weights_array[i]
          }
        }
      } else {
        for(let i=0; i<n_indices; i++){
          const bin = this.getbin(i, sample_array)
          if(bin >= 0 && bin < length){
            bincount[bin] += 1
          }
        }
      }
    } else {
      const n_indices = view_indices.length
      if(weights != null){
        const weights_array = this.source.get_column(weights)
        if (weights_array == null){
          throw ReferenceError("Column not defined: "+ weights)
        }
        for(let i=0; i<n_indices; i++){
          let j = view_indices[i]
          const bin = this.getbin(j, sample_array)
          if(bin >= 0 && bin < length){
            bincount[bin] += weights_array[j]
          }
        }
      } else {
        for(let i=0; i<n_indices; i++){
          const bin = this.getbin(view_indices[i], sample_array)
          if(bin >= 0 && bin < length){
            bincount[bin] += 1
          }
        }
      }
    }
    return bincount
  }

  getbin(idx: number, sample: number[][]): number{
      // This can be optimized using loop fission, but in our use case the data doeswn't change often, which means
      // that the cached bin indices are invalidated infrequently.
      // Another approach would be to cache index in the sorted array, this would require sorting the array, 
      // but would make subsequent hisogramming even quicker.
      const cached_value = this._bin_indices[idx]
      if(cached_value != -2) return cached_value
      let bin = 0

      for (let i = 0; i < this._nbins.length; i++) {
        const val = sample[i][idx];
        // Overflow bins
        if(val < this._range_min[i] || val > this._range_max[i]) {
          bin = -1
          break
        }

        // Make the max value inclusive
        if(val === this._range_max[i]){
          bin += this._nbins[i] * this._strides[i]
        } else {
          bin += ((val * this._transform_scale[i] - this._transform_origin[i]) | 0) * this._strides[i]
        }
      }
      this._bin_indices[idx] = bin
      return bin
  }

  public get_stride(idx: number): number{
    return this._strides[idx]
  }

}
