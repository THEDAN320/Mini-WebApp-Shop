import { axiosPublic } from "@/modules/common/api";

export async function getAllGoods(data: any) {
  const res = await axiosPublic.post(`/api/v1/goods/all/`, data);
  return res;
}

export async function createGood(data: any) {
  const res = await axiosPublic.post(`/api/v1/goods/`, data);
  return res;
}

export async function deleteGood(good_id: number) {
  const res = await axiosPublic.delete(`/api/v1/goods/${good_id}/`);
  return res;
}

export async function updateGood(good_id: number, data: any) {
  const res = await axiosPublic.patch(`/api/v1/goods/${good_id}/`, data);
  return res;
}

export async function getGoodById(good_id: number) {
  const res = await axiosPublic.get(`/api/v1/goods/${good_id}/`);
  return res;
}
