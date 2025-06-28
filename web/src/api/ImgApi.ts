import { service } from '@/utils/request'

export const uploadImgs = (data: FormData) => {
  return service({
    url: '/img/upload',
    method: 'post',
    data: data,
    responseType: 'json',
    headers: {
      'Content-Type': 'multipart/form-data',
      Accept: 'application/json',
    },
  })
}

export const getAllImgsInfo = () => {
  return service({
    url: '/img/get-all-imgs-info',
    method: 'get',
  })
}
