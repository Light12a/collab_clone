import axiosAPIServerIntance from "./axiosAPIServerIntance";
import { message } from 'antd'

async function handleRequest(method, link, body) {
    try {
        let data = await axiosAPIServerIntance[method](link, body)
        return Promise.resolve(data)
    } catch (error) {
        // handle error request
        console.dir(error)
        if (error.response?.status === 500) {
            message.error('This API fail b/c server')
        }
        if (error.response?.status === 401) {
            // LOGOUT
        }
        return Promise.reject(error)
    }
}


export const callAPI = async ({ method, path, body, }) => {
    try {
        let data = axiosAPIServerIntance[method ? method : 'post'](path, body)
        return data
    } catch (error) {
        // handle error request
        return Promise.reject(error)
    }
}

export const getUserConfigAPI = async (token) => {
    return handleRequest('post', '/get_user_config', { token })
}

export const loginAPI = async (body) => {
    return handleRequest('post', '/login', body)
}

export const reLoginAPI = async (body) => {
    return handleRequest('post', '/login', body)
}

export const setLoginLoadStateAPI = async (body) => {
    return handleRequest('post', '/login', body)
}

export const getUsersAPI = async (body) => {
    return handleRequest('post', '/get_users', body)
}

export const logoutAPI = async (body) => {
    return handleRequest('post', '/logout', body)
}

export const getSkillGroupAPI = async (body) => {
    return handleRequest('post', '/get_skill_groups', body)
}

export const getUserStateAPI = async (token) => {
    return handleRequest('post', '/get_user_state', { token })
}

export const applyStateAPI = async (body) => {
    return await handleRequest('post', '/apply_state', body)
}

export const getAwayReasonsAPI = async (token) => {
    return handleRequest('post', '/get_away_reasons', { token })
}

export const getCorrespondenceAPI = async (token) => {
    return handleRequest('post', '/get_correspondence_memo_list', { token })
}