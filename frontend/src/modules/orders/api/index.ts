import { axiosPublic } from "@/modules/common/api";

export async function getAllNumbers(data: any) {
  const res = await axiosPublic.post(`/api/v1/numbers-for-auto-delete-orders/all/`, data);
  return res;
}

export async function createNumber(data: any) {
  const res = await axiosPublic.post(`/api/v1/numbers-for-auto-delete-orders/`, data);
  return res;
}

export async function deleteNumber(address_id: number) {
  const res = await axiosPublic.delete(`/api/v1/numbers-for-auto-delete-orders/${address_id}/`);
  return res;
}

export async function getNumberById(address_id: number) {
  const res = await axiosPublic.get(`/api/v1/numbers-for-auto-delete-orders/${address_id}/`);
  return res;
}
