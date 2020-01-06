//index.js
//获取应用实例
const app = getApp();

Page({
  data: {
    
  },
  onLoad: function () {
    
  },
  handleInput: function (e) {
    let input = e.detail.value;
    let lastChar = input.charAt(input.length - 1);
    if (lastChar === '\n'){
      this.search(e.detail.value)
    }
  },
  search: function (e) {
    let q;
    if (e.constructor === String){
      q = e.substring(0, e.length-1);
    }
    else{
      q = e.detail.value.textarea
    }
    console.log("[index] search question: ", q)
    wx.showLoading({
      title: '分析中',

    })
    wx.request({
      url: 'http://localhost:5000/search',
      data: {
        'q': q,
        'ask': 'json'
      },
      success: function (result){
        wx.hideLoading()
        console.log("[index] result: ", result.data)
        wx.navigateTo({
          url: '../search/search?result=' + encodeURIComponent(JSON.stringify(result.data))
        })
      },
    })
  },
  about: function (e) {
    console.log('[index] about')
    wx.navigateTo({
      url: '../about/about',
    })
  }
});
