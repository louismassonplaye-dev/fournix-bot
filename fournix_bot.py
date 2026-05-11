from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8496620920:AAFh_NmNAAgT-nzBV1GQn7NZZz-s0IStq2M"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clavier = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤝 Faire de l'affiliation avec nous", callback_data="affiliation")],
        [InlineKeyboardButton("💰 J'ai vendu en tant qu'affilié", callback_data="vendu")],
        [InlineKeyboardButton("📦 Récupérer ma commande", callback_data="commande")],
        [InlineKeyboardButton("ℹ️ En savoir plus", callback_data="savoir")],
    ])
    await update.message.reply_text(
        "👋 Salut ! Tu veux savoir quoi ? 😊",
        reply_markup=clavier
    )

async def bouton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "affiliation":
        clavier = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Je veux devenir affilié !", callback_data="devenir_affilie")]
        ])
        await query.edit_message_text(
            "🤝 *Programme d'affiliation Fournix*\n\n"
            "1️⃣ Tu partages ton lien affilié 👇\n"
            "🔗 https://fournix.lovable.app/\n\n"
            "2️⃣ Des gens achètent via ton lien\n\n"
            "3️⃣ Tu gagnes une commission sur chaque vente 💸\n\n"
            "👇 Clique ci-dessous pour commencer !",
            reply_markup=clavier,
            parse_mode="Markdown"
        )

    elif query.data == "devenir_affilie":
        context.user_data["etape"] = "attente_mail_affiliation"
        await query.edit_message_text(
            "💌 Super ! Envoie-nous ton *adresse mail PayPal* 👇",
            parse_mode="Markdown"
        )

    elif query.data == "vendu":
        context.user_data["etape"] = "attente_mail_vendu"
        await query.edit_message_text(
            "💰 *Tu as fait une vente, félicitations !* 🎉\n\n"
            "Envoie-nous ton *adresse mail PayPal* pour recevoir ta commission 👇",
            parse_mode="Markdown"
        )

    elif query.data == "commande":
        context.user_data["etape"] = "attente_preuve"
        await query.edit_message_text(
            "📦 *Récupérer ma commande*\n\n"
            "Envoie-nous une *preuve d'achat* (screenshot) 👇",
            parse_mode="Markdown"
        )

    elif query.data == "savoir":
        clavier = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Contacter Fournix", url="https://t.me/fournix_1")]
        ])
        await query.edit_message_text(
            "ℹ️ *Tu veux savoir quoi en particulier ?* 🤔\n\n"
            "Clique ci-dessous pour nous contacter directement 👇",
            reply_markup=clavier,
            parse_mode="Markdown"
        )

async def message_texte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    etape = context.user_data.get("etape")
    texte = update.message.text

    if etape == "attente_mail_affiliation":
        context.user_data["etape"] = None
        await update.message.reply_text(
            f"✅ Ton mail PayPal *{texte}* est bien enregistré !\n\n"
            "🔗 Voici ton lien à partager :\nhttps://fournix.lovable.app/\n\n"
            "💸 Bonne vente ! Tape /start pour revenir au menu.",
            parse_mode="Markdown"
        )

    elif etape == "attente_mail_vendu":
        context.user_data["etape"] = None
        await update.message.reply_text(
            f"✅ Mail PayPal *{texte}* reçu !\n\n"
            "💰 Ton paiement arrive très bientôt !\n"
            "Tape /start pour revenir au menu.",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text("Tape /start pour voir le menu 😊")

async def photo_recue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    etape = context.user_data.get("etape")
    if etape == "attente_preuve":
        context.user_data["etape"] = None
        await update.message.reply_text(
            "📦 Merci pour ta preuve d'achat !\n\n"
            "⚠️ Ta commande va avoir du retard car nos usines sont en repos.\n\n"
            "🔎 Ton code de suivi : *8246381019746*\n\n"
            "📲 Tu seras tenu(e) au courant dès que ça repart !\n"
            "Tape /start pour revenir au menu.",
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(bouton))
    app.add_handler(MessageHandler(filters.PHOTO, photo_recue))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_texte))
    print("✅ Bot Fournix démarré !")
    app.run_polling()

if __name__ == "__main__":
    main()