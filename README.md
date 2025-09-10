# 🤖 Native Checker Bot

<div align="center">

![Native Checker Bot Logo](app/assets/logo.jpg)

**A smart Telegram bot that helps you write naturally and translate seamlessly**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)](https://aiogram.dev)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![Redis](https://img.shields.io/badge/Redis-Cache-red.svg)](https://redis.io)

</div>

## ✨ Features

- 🔧 **Message Refinement**: Transform your messages to sound more natural and polished
- 🌍 **Bilingual Support**: Seamless translation between English and Korean
- 🔊 **Text-to-Speech**: Convert refined messages to audio with natural voice
- ⚡ **Rate Limiting**: Smart request management with Redis-based caching
- 💰 **Premium Access**: Unlock unlimited requests with payment system
- 🎯 **User-Friendly**: Intuitive inline keyboards and interactive buttons

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Redis server
- OpenAI API key
- Telegram Bot Token
- OpenAI Assistant IDs (English & Korean)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/native_checker_bot.git
   cd native_checker_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   EN_ASSISTANT_ID=your_english_assistant_id
   KR_ASSISTANT_ID=your_korean_assistant_id
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_TELEGRAM_ID=your_admin_telegram_id
   REDIS_URL=localhost
   REDIS_PORT=6379
   ```

4. **Start Redis server**
   ```bash
   redis-server
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## 🎮 Usage

### Basic Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot and see welcome message |
| `/language` | Set your default language (English/Korean) |
| `/limit` | Check your current request limit status |
| `/buy` | View premium upgrade options |

### Interactive Features

- **🔊 Audio Generation**: Click the speaker icon to hear your refined message
- **🇺🇸/🇰🇷 Translation**: Instantly translate between English and Korean
- **⚡ Smart Refinement**: Just send any message to get it polished

### Rate Limiting

- **Free Users**: 3 requests per 5 minutes
- **Premium Users**: Unlimited requests
- **Auto-Reset**: Limits automatically reset after the time window

## 🏗️ Architecture

```
native_checker_bot/
├── app/
│   ├── assets/          # Static files (images)
│   ├── config.py        # Configuration management
│   ├── constants.py     # Bot messages and text constants
│   ├── handlers.py      # Telegram event handlers
│   ├── helpers.py       # Rate limiting and Redis utilities
│   ├── keyboards.py     # Inline and reply keyboards
│   └── utils.py         # OpenAI Assistant management
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## 🔧 Configuration

### OpenAI Assistants Setup

1. Create two OpenAI Assistants:
   - **English Assistant**: For refining English messages
   - **Korean Assistant**: For refining Korean messages and translations

2. Configure each assistant with appropriate instructions for:
   - Message refinement and natural language processing
   - Translation capabilities
   - Cultural context awareness

### Redis Configuration

The bot uses Redis for:
- **Rate Limiting**: Track user request counts and timestamps
- **Session Management**: Store user preferences and state
- **Caching**: Improve response times

## 💡 Key Components

### AssistantManager Class
Handles OpenAI Assistant interactions:
- Thread management
- Message processing
- Text-to-speech conversion
- Function calling support

### Rate Limiting System
- Configurable request limits per user
- Time-based reset mechanism
- Premium user support
- Redis-backed persistence

### Multilingual Support
- Dynamic language switching
- Context-aware translations
- Localized user interfaces

## 🛠️ Development

### Adding New Features

1. **New Commands**: Add handlers in `app/handlers.py`
2. **UI Elements**: Extend keyboards in `app/keyboards.py`
3. **Configuration**: Update `app/config.py` and `.env.example`
4. **Constants**: Add text constants in `app/constants.py`

### Testing

```bash
# Run the bot in development mode
python main.py

# Test specific components
python -m app.helpers  # Test rate limiting
```

## 📊 Monitoring

The bot includes built-in monitoring for:
- Request rate tracking
- Error handling and logging
- User activity patterns
- Premium subscription status

## 🔒 Security Features

- **Environment Variables**: Secure credential management
- **Rate Limiting**: Prevent abuse and spam
- **Admin Controls**: Administrative user management
- **Redis Security**: Secure data storage and caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [aiogram](https://aiogram.dev/) - Modern Telegram Bot framework
- [OpenAI](https://openai.com/) - GPT-4 and Assistant API
- [Redis](https://redis.io/) - In-memory data structure store

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/native_checker_bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/native_checker_bot/discussions)
- **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ for better communication**

[⭐ Star this repo](https://github.com/yourusername/native_checker_bot) • [🐛 Report Bug](https://github.com/yourusername/native_checker_bot/issues) • [💡 Request Feature](https://github.com/yourusername/native_checker_bot/issues)

</div>
