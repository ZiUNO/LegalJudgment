// pages/search/search.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    result: {}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let result = JSON.parse(options.result);
    this.setData({
      'result.predictions': {
        id: 'prediction',
        open: true,
        value: result.predictions
      },
      'result.articles': {
        id: 'articles',
        open: false,
        value: result.articles
      },
      'result.similarCases': {
        id: 'similarCases',
        open: false,
        value: result.similarCases
      }
    })
    console.log("[search] result: ", this.data.result)
  },
  kindToggle: function (e) {
    var id = e.currentTarget.id, result = this.data.result;
    if (e.currentTarget.id === result.predictions.id){
      result.articles.open = false;
      result.similarCases.open = false;
      result.predictions.open = true;
    }
    else if (e.currentTarget.id === result.articles.id){
      result.articles.open = true;
      result.similarCases.open = false;
      result.predictions.open = false;
    }
    else{
      result.articles.open = false;
      result.similarCases.open = true;
      result.predictions.open = false;
    }
    this.setData({
      result: result
    });
  }
})