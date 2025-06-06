// AWS Bedrock Translation App JavaScript

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log("文档已加载，准备绑定事件");
    
    // 评分系统
    setupRatingSystem();
    
    // 凭证切换
    setupCredentialsToggle();
    
    // 尝试加载统计数据
    try {
        loadRatingStats();
    } catch (e) {
        console.error("Error loading initial stats:", e);
    }
    
    // 绑定刷新统计按钮
    const refreshStatsBtn = document.getElementById('refresh-stats');
    if (refreshStatsBtn) {
        refreshStatsBtn.addEventListener('click', loadRatingStats);
    }
});

// 设置评分系统
function setupRatingSystem() {
    // 绑定星星点击事件
    const ratingStars = document.querySelectorAll('.rating-star');
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');
            rateTranslation(rating);
        });
    });
    
    // 绑定提交按钮点击事件
    const submitRatingBtn = document.getElementById('submit-rating');
    if (submitRatingBtn) {
        submitRatingBtn.addEventListener('click', submitRating);
    }
}

// 评分函数
function rateTranslation(rating) {
    console.log("评分函数被调用，评分：" + rating);
    
    // 更新星星显示
    const stars = document.querySelectorAll('.rating-star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove("fa-star-o");
            star.classList.add("fa-star");
        } else {
            star.classList.remove("fa-star");
            star.classList.add("fa-star-o");
        }
    });
    
    // 更新文本和启用提交按钮
    const ratingText = document.getElementById("rating-text");
    const submitBtn = document.getElementById("submit-rating");
    
    if (ratingText) ratingText.textContent = rating + "/5 星";
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.setAttribute('data-rating', rating);
    }
}

// 提交评分函数
function submitRating() {
    const submitBtn = document.getElementById("submit-rating");
    const rating = submitBtn.getAttribute('data-rating');
    console.log("提交评分函数被调用，评分：" + rating);
    
    // 获取翻译数据
    const sourceText = document.getElementById("original-text").textContent;
    const translatedText = document.getElementById("translated-text").textContent;
    const sourceLanguage = document.getElementById("source_language").value;
    const targetLanguage = document.getElementById("target_language").value;
    const modelId = document.getElementById("model_id").value;
    
    // 准备评分数据
    const ratingData = {
        source_text: sourceText,
        translated_text: translatedText,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        model_id: modelId,
        rating: parseInt(rating)
    };
    
    // 发送AJAX请求
    fetch('/submit_rating', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(ratingData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('评分提交失败');
        }
        return response.json();
    })
    .then(data => {
        alert("评分提交成功，谢谢您的反馈！");
        
        // 重置评分界面
        const stars = document.querySelectorAll('.rating-star');
        stars.forEach(star => {
            star.classList.remove("fa-star");
            star.classList.add("fa-star-o");
        });
        
        const ratingText = document.getElementById("rating-text");
        if (ratingText) ratingText.textContent = "请选择评分";
        
        if (submitBtn) submitBtn.disabled = true;
        
        // 刷新统计
        loadRatingStats();
    })
    .catch(error => {
        alert("评分提交失败: " + error.message);
    });
}

// 凭证切换函数
function toggleCredentials() {
    const useProfile = document.getElementById('use_profile').checked;
    const accessKey = document.getElementById('access_key');
    const secretKey = document.getElementById('secret_key');
    
    if (useProfile) {
        accessKey.disabled = true;
        secretKey.disabled = true;
    } else {
        accessKey.disabled = false;
        secretKey.disabled = false;
    }
}

// 加载评分统计
function loadRatingStats() {
    const granularity = document.getElementById('stats-granularity')?.value || 'day';
    
    fetch(`/rating_stats?granularity=${granularity}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load rating stats');
            }
            return response.json();
        })
        .then(data => {
            // 渲染图表
            if (typeof renderTrendChart === 'function') {
                renderTrendChart(data.time_series, granularity);
                renderDistributionChart(data.rating_distribution);
                renderLanguagePairChart(data.language_pairs);
                renderModelChart(data.models);
                renderInsights(data.insights);
            } else {
                console.warn('Chart rendering functions not available');
            }
        })
        .catch(error => {
            console.error('Failed to load rating stats:', error);
        });
}
