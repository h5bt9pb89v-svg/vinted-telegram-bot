
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Benvenuto in Vinted Deal Finder!\n\n"
        "Comandi disponibili:\n"
        "/calcola 12 35 3\n"
        "/soglia 10\n"
        "/aiuto\n\n"
        "Calcolo del profitto stimato: "
        "rivendita - acquisto - costi extra."
    )


async def calcola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) not in (2, 3):
            raise ValueError

        acquisto = float(context.args[0].replace(",", "."))
        rivendita = float(context.args[1].replace(",", "."))
        costi = (
            float(context.args[2].replace(",", "."))
            if len(context.args) == 3 else 0
        )

        if min(acquisto, rivendita, costi) < 0:
            raise ValueError

        profitto = rivendita - acquisto - costi
        roi = profitto / (acquisto + costi) * 100 if acquisto + costi else 0
        soglia = context.user_data.get("soglia", 10)
        esito = "✅ Sopra la soglia" if profitto >= soglia else "⚠️ Sotto la soglia"

        await update.message.reply_text(
            f"📊 RISULTATO\n\n"
            f"Acquisto: €{acquisto:.2f}\n"
            f"Rivendita prevista: €{rivendita:.2f}\n"
            f"Costi extra: €{costi:.2f}\n"
            f"Profitto stimato: €{profitto:.2f}\n"
            f"ROI stimato: {roi:.1f}%\n\n"
            f"{esito}"
        )
    except ValueError:
        await update.message.reply_text(
            "Formato corretto:\n/calcola 12 35 3\n"
            "I numeri indicano acquisto, rivendita e costi extra."
        )


async def soglia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        valore = float(context.args[0].replace(",", "."))
        if valore < 0:
            raise ValueError
        context.user_data["soglia"] = valore
        await update.message.reply_text(
            f"Soglia impostata a €{valore:.2f}."
        )
    except (ValueError, IndexError):
        await update.message.reply_text("Usa il comando /soglia 10")


async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aiuto", start))
    app.add_handler(CommandHandler("calcola", calcola))
    app.add_handler(CommandHandler("soglia", soglia))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
