import { axiosPublic } from "@/modules/common/api";

export async function getAllOrders(data: any) {
  const res = await axiosPublic.post(`/api/v1/orders/all/`, data);
  return res;
}

export async function createOrder(data: any) {
  const res = await axiosPublic.post(`/api/v1/orders/`, data);
  return res;
}

export async function deleteOrder(order_id: number) {
  const res = await axiosPublic.delete(`/api/v1/orders/${order_id}/`);
  return res;
}

export async function updateOrder(order_id: number, data: any) {
  const res = await axiosPublic.patch(`/api/v1/orders/${order_id}/`, data);
  return res;
}

export async function getOrderById(order_id: number) {
  const res = await axiosPublic.get(`/api/v1/orders/${order_id}/`);
  return res;
}
