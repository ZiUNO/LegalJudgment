// pages/case/case.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    caseDetail: {}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this
    console.log("[case] caseType: ", options.caseType)
    console.log("[case] uniqid: ", options.uniqid)
    wx.request({
      url: 'http://localhost:5000/case',
      data: {
        'type': options.caseType,
        'uniqid': options.uniqid,
        'ask': 'json'
      },
      success: function(res){
        let caseDetail = res.data;
        let contents = caseDetail.contents;
        for (let i = 1, len=contents.length; i<len; ++i){
          contents[i].open = false;
        }
        contents[0].open = true;
        caseDetail.contents = contents
        that.setData({
          caseDetail: caseDetail
        })
        console.log('[case] caseDetail: ', caseDetail)
      }
    })
  },
  kindToggle: function (e) {
    var id = e.currentTarget.id, contents = this.data.caseDetail.contents;
    for (var i = 0, len = contents.length; i < len; ++i) {
      if (i == id) {
        contents[i].open = !contents[i].open
      } else {
        contents[i].open = false
      }
    }
    this.setData({
      'caseDetail.contents': contents
    });
    console.log('[case] kindToggle: ', e.currentTarget.id)
  }
})