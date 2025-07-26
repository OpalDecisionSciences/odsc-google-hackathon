# 🔑 API Setup Guide - Enhanced Business Intelligence

This system provides **graceful degradation** - it works perfectly without API keys but offers enhanced functionality when they're available.

## 🚀 **Current Functionality (No Additional APIs Required)**

✅ **Works RIGHT NOW with just GEMINI_API_KEY:**
- Real financial data (Yahoo Finance)
- Live news sentiment (Google News)
- Company information (Wikipedia)
- Industry trends analysis
- Competitive financial comparison
- Agent orchestration with live data

## 🔑 **Optional API Enhancements**

### **1. Twitter/X API** 
**Enhances**: Real-time social media monitoring
```bash
# Get from: https://developer.twitter.com/
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
```
**Cost**: $100/month basic tier  
**Benefit**: Real social media mentions, sentiment, engagement metrics

### **2. Reddit API**
**Enhances**: Community sentiment analysis
```bash
# Get from: https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_username_here
REDDIT_PASSWORD=your_password_here
```
**Cost**: Free tier available  
**Benefit**: Community discussions, product sentiment, subreddit analysis

### **3. News API**
**Enhances**: Comprehensive news analysis
```bash
# Get from: https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here
```
**Cost**: Free tier (1000 requests/day)  
**Benefit**: More news sources, better sentiment analysis, trending keywords

### **4. LinkedIn API** 
**Enhances**: Professional network analysis
```bash
# Get from: https://developer.linkedin.com/
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
```
**Cost**: Varies by usage  
**Benefit**: Professional network insights (limited due to LinkedIn restrictions)

### **5. Alpha Vantage API**
**Enhances**: Advanced financial metrics
```bash
# Get from: https://www.alphavantage.co/
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```
**Cost**: Free tier available  
**Benefit**: Technical indicators, advanced financial analytics

## 🛠 **Setup Instructions**

### **1. Copy Environment Template**
```bash
cp .env.example .env
```

### **2. Add Your API Keys**
Edit `.env` file and add any API keys you have:
```bash
# Required
GEMINI_API_KEY=your_gemini_key_here

# Optional (add as many as you have)
TWITTER_BEARER_TOKEN=your_twitter_token_here
REDDIT_CLIENT_ID=your_reddit_id_here
NEWS_API_KEY=your_news_key_here
# ... etc
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt

# Optional: Install social media libraries if you have API keys
pip install tweepy praw requests-oauthlib
```

### **4. Launch System**
```bash
python demo_ui.py
```

## 📊 **API Status Display**

The system shows exactly which APIs are active:

```
🔑 API Status: Twitter=True, Reddit=False, News=True, LinkedIn=False
📊 Active APIs: twitter, news
📋 API Enhancement: 2/5 APIs active
```

## 🎯 **For Google Hackathon Judges**

**Without additional APIs**: Still revolutionary compared to other demos
- Real financial data analysis
- Live news sentiment
- True agent orchestration
- Dynamic business context

**With Google's APIs**: Production-ready business intelligence platform
- Real-time social media monitoring
- Comprehensive sentiment analysis
- Professional network insights
- Advanced financial metrics

## 🔒 **Security Best Practices**

- Never commit API keys to version control
- Use `.env` file for local development
- Use environment variables for production
- Rotate API keys regularly
- Monitor API usage and costs

## 🚨 **Rate Limiting & Costs**

The system respects API rate limits:
- **Twitter API**: 300 requests/15min
- **News API**: 1000 requests/day (free)
- **Reddit API**: 60 requests/minute
- **Alpha Vantage**: 5 requests/minute (free)

## 🎬 **Demo Strategy**

**For judges without API keys**: 
- Emphasize the working financial intelligence
- Show real company analysis (NVIDIA, AMD, Tesla)
- Demonstrate agent orchestration

**For judges with API keys**:
- Show enhanced social media intelligence
- Demonstrate comprehensive sentiment analysis
- Highlight production-ready capabilities

---
**🏆 The system is designed to impress at every level - from basic functionality to full API integration!**