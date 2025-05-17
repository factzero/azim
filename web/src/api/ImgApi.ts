import { service } from '@/utils/request'

export const uploadImgs = (data: FormData) => {
  return service({
    url: '/img/upload',
    method: 'post',
    data: data,
    responseType: 'blob',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const getAllImgsInfo = () => {
  return service({
    url: '/img/get-all-imgs-info',
    method: 'get',
  })
}
