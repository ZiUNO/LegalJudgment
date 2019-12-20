//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    
  },
  onLoad: function () {
    
  },
  handleInput: function (e) {
    let input = e.detail.value
    let lastChar = input.charAt(input.length - 1)
    if (lastChar == '\n'){
      this.search(e.detail.value)
    }
  },
  search: function (e) {
    let q = ''
    if (e.constructor === String){
      q = e
    }
    else{
      q = e.detail.value
    }
    console.log(e)
    // wx.request({
    //   url: 'http://localhost:5000/search',
    //   data: {
    //     'q': e
    //   },
    //   success: function (result){
    //     console.log(result)
    //   }
    // })
  },
  about: function (e) {
    console.log(e)
  }
})
