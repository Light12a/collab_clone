import axios from "axios";

const baseURL = "https://18.179.96.129"

const axiosAPIServerIntance = axios.create({
    baseURL
})
export default axiosAPIServerIntance