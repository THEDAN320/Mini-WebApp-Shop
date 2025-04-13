import axios from "axios";


const APIUrl =
  process.env.NODE_ENV === "dev" ? "http://localhost:8000" : process.env.VUE_APP_API_ROOT;

const axiosPublic = axios.create({
  baseURL: APIUrl,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});

export { APIUrl, axiosPublic };
