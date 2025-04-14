export type typeSortingOrder = "asc" | "desc" | string;

// export interface IColumnData {
//   title: string;
//   key: string;
//   isSortable: boolean;

//   sortingOrder?: typeSortingOrder;
//   prioritySortingOrder?: number;
// }

export interface IColumnData {
  title: string;
  key: string;
  isSortable: boolean;
}

export interface IExtentedColumnData extends IColumnData {
  sortingOrder?: typeSortingOrder;
}
