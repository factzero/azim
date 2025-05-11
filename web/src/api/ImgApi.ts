import { service } from '@/utils/request'

export const uploadImgs = (data) => {
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
