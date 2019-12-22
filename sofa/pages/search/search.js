// pages/search/search.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        predictions: {},
        articles: {},
        similarCases: {}
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        let result = JSON.parse(options.result);
        this.setData({
            predictions: {
                id: 'prediction',
                open: true,
                value: result.predictions
            },
            articles: {
                id: 'articles',
                open: false,
                value: result.articles
            },
            similarCases: {
                id: 'similarCases',
                open: false,
                authcase: result.similarCases.authcase,
                case: result.similarCases.case
            }
        })
        console.log("[search] prediction: ", this.data.predictions)
        console.log("[search] articles: ", this.data.articles)
        console.log("[search] similarCases: ", this.data.similarCases)
    },
    kindToggle: function (e) {
        let id = e.currentTarget.id
        let predictions = this.data.predictions
        let articles = this.data.articles
        let similarCases = this.data.similarCases
        let toDisplay = 0;
        if (e.currentTarget.id === predictions.id) {
            articles.open = false;
            similarCases.open = false;
            predictions.open = true;
            toDisplay = predictions;
        } else if (e.currentTarget.id === articles.id) {
            articles.open = true;
            similarCases.open = false;
            predictions.open = false;
            toDisplay = articles;
        } else if (e.currentTarget.id === similarCases.id) {
            articles.open = false;
            similarCases.open = true;
            predictions.open = false;
            toDisplay = similarCases;
        }
        console.log('[search] to see ', toDisplay)
        this.setData({
            articles: articles,
            predictions: predictions,
            similarCases: similarCases
        });
    },
    onReady: function (e) {
        wx.hideLoading()
    }
})