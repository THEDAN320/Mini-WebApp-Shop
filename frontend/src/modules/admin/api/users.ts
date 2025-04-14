import { axiosPublic } from "@/modules/common/api";

export async function getAllUsers(data: any) {
  const res = await axiosPublic.post(`/api/v1/users/all/`, data);
  return res;
}

export async function createUser(data: any) {
  const res = await axiosPublic.post(`/api/v1/users/`, data);
  return res;
}

export async function deleteUser(user_id: number) {
  const res = await axiosPublic.delete(`/api/v1/users/${user_id}/`);
  return res;
}

export async function updateUser(user_id: number, data: any) {
  const res = await axiosPublic.patch(`/api/v1/users/${user_id}/`, data);
  return res;
}

export async function getUserById(user_id: number) {
  const res = await axiosPublic.get(`/api/v1/users/${user_id}/`);
  return res;
}
