# Changelog - Major Update: YooMoney Removal, Trial System Updates, and Complete Multilingual Support

## Major Changes

### 0. Complete Multilingual Support ✅
- **Full English/Russian support throughout entire bot**
- Language preference stored in database and persists across sessions
- Bot responses (LLM) generate in user's selected language
- All trial, subscription, and payment messages multilingual
- Girl names, descriptions, and professions fully translated
- English users get 100% English experience, Russian users get 100% Russian experience

### 1. Removed YooMoney Payment System
- Deleted `yoomoney.py`, `yoomoney_links.py`, and all YooMoney documentation files
- Removed all YooMoney imports and references from the codebase
- Payment system now uses only Telegram Stars

### 2. New Trial System with Daily Message Limit
- **Trial period now includes only 15 messages per day**
- Messages reset every 24 hours
- When limit is reached, user sees message with options to:
  - Wait for reset (next day)
  - Purchase monthly subscription (100 ⭐)
  - Purchase lifetime access (999 ⭐)

### 3. Added Lifetime Access Purchase
- New purchase option: **Lifetime Access for 999 stars**
- Lifetime access provides unlimited messages and all features permanently
- Can be purchased through the premium subscription menu

### 4. Updated Onboarding
- Added warning about trial period limitations when user starts trial
- Mentions that trial = 15 messages per day
- Explains message limit resets daily

### 5. Updated Subscription Menus
- Removed YooMoney payment options
- Added information about @PremiumBot for purchasing stars
- Replaced all "buy subscription" options with Telegram Stars payment buttons

## Database Changes

### New Table Fields in `stats`:
- `daily_messages_count` - Tracks messages sent today
- `last_message_date` - Last date a message was sent

### New Access Type:
- `lifetime` - Added to access table for lifetime access type

### New Functions in `db.py`:
- `check_daily_message_limit(user_id)` - Checks if user can send message
- `increment_daily_message_count(user_id)` - Increments daily counter
- `has_lifetime_access(user_id)` - Checks for lifetime access
- `grant_lifetime_access(user_id)` - Grants lifetime access

## Updated Files

1. `bot/db.py` - Added daily message tracking and lifetime access support
2. `bot/main.py` - Removed YooMoney imports, added daily message limit check in chat handler
3. `bot/stars_payment_handlers.py` - Added handlers for monthly and lifetime subscriptions
4. `bot/telegram_stars.py` - Added lifetime access payment support
5. `bot/payment_system.py` - Removed YooMoney references
6. `bot/payment_handlers.py` - Updated to remove YooMoney references
7. `bot/webhook_server.py` - Deprecated (no longer used)

## Payment Flow

### Monthly Subscription (100 ⭐)
1. User clicks "💎 Подписка на месяц (100 ⭐)"
2. Telegram invoice is sent
3. User pays with stars
4. User gets 30 days of premium access

### Lifetime Access (999 ⭐)
1. User clicks "🚀 Доступ навсегда (999 ⭐)"
2. Telegram invoice is sent
3. User pays with stars
4. User gets permanent access (no expiration)

## Trial Period Behavior

### First 15 Messages (Trial)
- User can send up to 15 messages per day
- Counter resets every 24 hours
- No restrictions on which features to use

### After 15 Messages (Limit Reached)
- User sees message with:
  - Information about limit being reached
  - Options to purchase subscription or lifetime access
  - Information about @PremiumBot for buying stars
- User cannot send more messages until:
  - Next day (counter resets), OR
  - User purchases subscription/lifetime access

## User Communication Updates

### When Trial Starts
Users see warning:
```
⚠️ ВАЖНО: Пробный период включает в себя только 15 текстовых сообщений боту в день.

Каждый день эти 15 сообщений обновляются...
```

### When Limit Reached
Users see:
```
❌ Лимит сообщений достигнут

Вы отправили 15 сообщений сегодня...
💎 Звезды можно приобрести в @PremiumBot
```

### In Premium Subscription Menu
Always mentions: "💎 Звезды можно приобрести в @PremiumBot"

## Technical Notes

- Daily message tracking automatically resets at midnight (when date changes)
- Lifetime access users bypass all daily message limits
- Monthly subscription users bypass daily message limits (unlimited messages)
- All payment processing now handled through Telegram Stars handlers

