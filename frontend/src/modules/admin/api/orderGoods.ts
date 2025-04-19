import { axiosPublic } from "@/modules/common/api";

export async function getAllOrderGoods(data: any) {
  const res = await axiosPublic.post(`/api/v1/order_goods/all/`, data);
  return res;
}

export async function createOrderGoods(data: any) {
  const res = await axiosPublic.post(`/api/v1/order_goods/`, data);
  return res;
}

export async function deleteOrderGoods(order_good_id: number) {
  const res = await axiosPublic.delete(`/api/v1/order_goods/${order_good_id}/`);
  return res;
}

export async function updateOrderGoods(order_good_id: number, data: any) {
  const res = await axiosPublic.patch(`/api/v1/order_goods/${order_good_id}/`, data);
  return res;
}

export async function getOrderGoodsById(order_good_id: number) {
  const res = await axiosPublic.get(`/api/v1/order_goods/${order_good_id}/`);
  return res;
}
