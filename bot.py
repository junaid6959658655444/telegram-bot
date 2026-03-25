const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');

const token = "8693735939:AAFlQiKOCCvwJaylnhqC_MYvWyW2S0dwx64";
const ADMIN_ID = 6414433469; // আপনার ID

const bot = new TelegramBot(token, { polling: true });

// ডাটাবেস ফাইল
let users = [];

if (fs.existsSync('users.json')) {
  users = JSON.parse(fs.readFileSync('users.json'));
}

// Save function
function saveUsers() {
  fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
}

// Start command
bot.onText(/\/start/, (msg) => {
  const id = msg.chat.id;

  if (!users.includes(id)) {
    users.push(id);
    saveUsers();
  }

  bot.sendMessage(id, "👋 Welcome to Telecom Support\nআপনার সমস্যা লিখুন...");
});

// User Message → Admin
bot.on('message', (msg) => {

  if (msg.chat.id !== ADMIN_ID) {

    bot.forwardMessage(ADMIN_ID, msg.chat.id, msg.message_id);

    bot.sendMessage(msg.chat.id, "✅ আপনার মেসেজ পাঠানো হয়েছে, অপেক্ষা করুন।");

  }
});

// Admin Reply → User
bot.on('reply_to_message', (msg) => {

  if (msg.chat.id === ADMIN_ID) {

    if (!msg.reply_to_message.forward_from) return;

    const userId = msg.reply_to_message.forward_from.id;

    bot.sendMessage(userId, "📩 Support Reply:\n" + msg.text);
  }
});

// 📢 Broadcast
bot.onText(/\/broadcast (.+)/, (msg, match) => {

  if (msg.chat.id !== ADMIN_ID) return;

  const text = match[1];

  users.forEach(id => {
    bot.sendMessage(id, "📢 " + text).catch(() => {});
  });

  bot.sendMessage(ADMIN_ID, "✅ Broadcast Sent");
});

// 🚫 Ban
let banned = [];

bot.onText(/\/ban (\d+)/, (msg, match) => {

  if (msg.chat.id !== ADMIN_ID) return;

  const userId = parseInt(match[1]);

  if (!banned.includes(userId)) {
    banned.push(userId);
  }

  bot.sendMessage(ADMIN_ID, "🚫 User Banned");
});

// ✅ Unban
bot.onText(/\/unban (\d+)/, (msg, match) => {

  if (msg.chat.id !== ADMIN_ID) return;

  const userId = parseInt(match[1]);

  banned = banned.filter(id => id !== userId);

  bot.sendMessage(ADMIN_ID, "✅ User Unbanned");
});

// Block banned users
bot.on('message', (msg) => {

  if (banned.includes(msg.chat.id)) return;

});
