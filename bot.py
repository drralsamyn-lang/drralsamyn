import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =================================================================
# مفتاح البوت السري (BOT_TOKEN)
# =================================================================
# تأكد من استبدال هذا المفتاح بمفتاح البوت الخاص بك
BOT_TOKEN = "8580351979:AAE3rRb1MHtV4r9eqcf6Mm97i-4K_NWDMuU" 
# =================================================================

# =================================================================
# قاعدة بيانات الملحقات (تم تحديث رابط طبقات الرواة)
# =================================================================
attachments_data = {
    "AMSAR": {
        "url": "https://drive.google.com/file/d/18N6IrsflyYJ059NrjYPxWdF1iRYBe_x_/view?usp=sharing",
        "name": "أمصار الصحابة وأهم الرواة عنهم",
        "caption": "رابط خارطة الأمصار وأهم الرواة عنهم (Google Drive):"
    },
    "TABAQAT": {
        # تم تحديث الرابط هنا
        "url": "https://drive.google.com/file/d/1zMyt2hPxJ63NDTDUBReKeLnuaEUwnIjE/view?usp=sharing", 
        "name": "طبقات رواة الحديث",
        "caption": "رابط طبقات رواة الحديث (Google Drive):"
    },
    "STUDENT_BIOS": {
        "url": "https://drive.google.com/drive/folders/1FGosuk2ABesqjcMfCviA3z422NbIOEEi?usp=sharing",
        "name": "التراجم المعدة من قبل الطالبات",
        "caption": "مجلد تراجم الطالبات (Google Drive):"
    }
}


# =================================================================
# قاعدة بيانات العلماء (Scholars Data) - الطبقة السابعة
# =================================================================
scholars_data = {
    "L7": {  # <--- المفتاح الداخلي للطبقة السابعة
        1: {
            "اسم_العالم": "الإمام الزهري",
            "تعريف بسيط عنه": """محمد بن مسلم بن عبيد الله بن عبدالله بن شهاب...""",
            "علمه ومكانته": """معروف بعلمه الواسع ومكانته الرفيعة...""",
            "شيوخه: ": """تلقى الإمام الزهري العلم عن شيوخ كثيرين...""",
            "تلاميذه": """من أشهرهم: مالك بن أنس، محمد بن إسحاق...""",
            "أقوال العلماء": """أبو صالح، عن الليث بن سعد، قال: ما رأيت عالماً قط أجمع من ابن شهاب...""",
            "وفاته": """ توفي الإمام الزهري بعد حياة علمية رفيعة...""",
        },
        2: {
            "اسم_العالم": "الإمام قتادة السدوسي",
            "تعريف بسيط عنه": """قتادة بن دعامة بن قتادة السدوسي البصري...""",
        },
        3: {
            "اسم_العالم": "الإمام أيوب السختياني",
            "تعريف بسيط عنه": "أيوب بن أبي تيمية كيسان السختياني...",
        },
        4: {
            "اسم_العالم": "الإمام عمرو بن دينار",
            "تعريف بسيط عنه": """هو أبو محمد، عمرو بن دينار بن عمرو الجمحي المكي...""",
        },
        5: {
            "اسم_العالم": "الإمام يونس بن يزيد",
            "تعريف بسيط عنه": "يونس بن يزيد بن أَبي النجاد...",
        },
        6: {
            "اسم_العالم": "الإمام الأعمش",
            "تعريف بسيط عنه": " أبو محمد سُليمان بن مِهرَان الأعمش الأسدي الكاهلي...",
        },
        7: {
            "اسم_العالم": "الإمام سفيان بن عيينة",
            "تعريف بسيط عنه": """سفيان بن عيينة بن أبي عمران ميمون مولى محمد بن مُزاحم...""",
        },
        8: {
            "اسم_العالم": "الإمام سفيان الثوري",
            "تعريف بسيط عنه": """هو سفيان بن سعيد الثوري الفقيه المحدث عالم التفسير...""",
        },
        9: {
            "اسم_العالم": "الإمام مالك بن أنس",
            "تعريف بسيط عنه": """هو مالك بن أنس بن مالك بن أبي عامر بن عمرو بن الحارث...""",
        }
    }
}
# =================================================================
# دوال إنشاء لوحات المفاتيح (Inline Keyboards)
# =================================================================

def create_level_menu() -> InlineKeyboardMarkup:
    """تنشئ لوحة مفاتيح (Keyboard) لاختيار الطبقة والأقسام الجديدة."""
    keyboard = [
        # الصف الأول: الأقسام الجديدة
        [
            InlineKeyboardButton("🔗 ملحقات", callback_data="ATTACHMENTS_MENU"),
            InlineKeyboardButton("📝 التراجم المعدة من قبل الطالبات", callback_data="STUDENT_BIOS_SEND")
        ],
        # الصف الثاني: الطبقة السابعة
        [
            InlineKeyboardButton("الطبقة السابعة", callback_data="LEVEL_L7")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_attachments_menu() -> InlineKeyboardMarkup:
    """تنشئ لوحة مفاتيح لقسم الملحقات الفرعي، بأزرار URL مباشرة."""
    keyboard = [
        # زر أمصار الصحابة (URL مباشرة)
        [InlineKeyboardButton(attachments_data["AMSAR"]["name"], url=attachments_data["AMSAR"]["url"])],
        # زر طبقات الرواة (URL مباشرة)
        [InlineKeyboardButton(attachments_data["TABAQAT"]["name"], url=attachments_data["TABAQAT"]["url"])],
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="MENU")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_scholar_menu(scholarship_level: str) -> InlineKeyboardMarkup:
    """تنشئ لوحة مفاتيح (Keyboard) بأسماء العلماء لطبقة معينة."""
    keyboard = []
    if scholarship_level in scholars_data:
        
        row = []
        for scholar_id, scholar_data in scholars_data[scholarship_level].items(): 
            name = scholar_data["اسم_العالم"] 
            callback_data = f"SCHOLAR_{scholarship_level}_{scholar_id}" 
            row.append(InlineKeyboardButton(name, callback_data=callback_data))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row: 
            keyboard.append(row)

    # زر العودة للقائمة الرئيسية
    keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="MENU")])
    return InlineKeyboardMarkup(keyboard)

def create_scholar_info_menu(scholar_id: int, level_key: str) -> InlineKeyboardMarkup:
    """تنشئ لوحة مفاتيح بجميع حقول معلومات العالم."""
    keyboard = []
    
    scholar_data = scholars_data.get(level_key, {}).get(scholar_id, {})
    
    # قائمة حقول المعلومات (باستثناء 'اسم_العالم')
    info_fields = [k for k in scholar_data.keys() 
                   if k not in ["اسم_العالم"]]
    
    row = []
    for field in info_fields:
        field_key_safe = field.replace(' ', '`').replace(':', '_') 
        callback_data = f"INFO_{level_key}_{scholar_id}_{field_key_safe}"
        row.append(InlineKeyboardButton(field, callback_data=callback_data))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # زر العودة لقائمة علماء الطبقة
    back_data = f"LEVEL_{level_key}"
    keyboard.append([InlineKeyboardButton("🔙 العودة لقائمة علماء الطبقة", callback_data=back_data)])
    
    return InlineKeyboardMarkup(keyboard)

# =================================================================
# دوال معالجة الأوامر والردود (Command Handlers)
# =================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة الأمر /start وإظهار القائمة الرئيسية."""
    menu_keyboard = create_level_menu()
    
    text = "📚 **أهلاً بك في بوت تراجم العلماء**\n\nاختر القسم الذي تود تصفحه:"
    
    await update.message.reply_text(
        text,
        reply_markup=menu_keyboard,
        parse_mode='Markdown'
    )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة استدعاءات الأزرار المضمنة (Inline Keyboard)."""
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat_id

    # --- معالجة الأقسام الرئيسية الجديدة ---
    
    # 1. قائمة الملحقات (ATTACHMENTS_MENU)
    if data == "ATTACHMENTS_MENU":
        menu = create_attachments_menu()
        text = "🔗 **قسم الملحقات**\n\nاختر الملف الذي تود تحميله (الروابط تفتح مباشرة):"
        await query.edit_message_text(text=text, reply_markup=menu, parse_mode='Markdown')
        return

    # 2. إرسال رابط تراجم الطالبات (STUDENT_BIOS_SEND)
    if data == "STUDENT_BIOS_SEND":
        bio_data = attachments_data['STUDENT_BIOS']
        
        # إنشاء زر URL للرابط
        url_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📂 فتح مجلد التراجم", url=bio_data['url'])],
            [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="MENU")]
        ])
        
        text = (
            f"📝 **{bio_data['name']}**\n\n"
            f"{bio_data['caption']} اضغط على الزر أدناه لفتح المجلد:"
        )
        
        await query.edit_message_text(text=text, reply_markup=url_button, parse_mode='Markdown')
        return

    # --- معالجة الأقسام القديمة (القائمة الرئيسية والتراجم) ---

    # 3. العودة للقائمة الرئيسية (MENU)
    if data == "MENU":
        menu_keyboard = create_level_menu()
        text = "📚 **أهلاً بك في بوت تراجم العلماء**\n\nاختر القسم الذي تود تصفحه:"
        await query.edit_message_text(text=text, reply_markup=menu_keyboard, parse_mode='Markdown')
        return

    # 4. اختيار طبقة معينة (LEVEL_L7)
    if data.startswith("LEVEL_"): 
        level_key = data.split("_")[-1]
        
        scholar_menu = create_scholar_menu(level_key)
        level_display_name = f"الطبقة {level_key.replace('L', ' السابعة')}" 
        
        text = f"**{level_display_name}**\n\nاختر العالم الذي تود قراءة ترجمته:"
        await query.edit_message_text(text=text, reply_markup=scholar_menu, parse_mode='Markdown')
        return

    # 5. اختيار عالم معين (SCHOLAR_L7_1)
    if data.startswith("SCHOLAR_"):
        parts = data.split("_")
        level_key = parts[1]
        scholar_id = int(parts[2])
        scholar_data = scholars_data.get(level_key, {}).get(scholar_id, {})
        scholar_name = scholar_data.get("اسم_العالم", "عالم غير معروف")
        
        info_menu = create_scholar_info_menu(scholar_id, level_key) 
        text = f"👤 **ترجمة: {scholar_name}**\n\nاختر تفاصيل الترجمة التي تريد قراءتها:"
        await query.edit_message_text(text=text, reply_markup=info_menu, parse_mode='Markdown')
        return

    # 6. اختيار حقل معلومات معين (INFO_L7_1_...)
    if data.startswith("INFO_"):
        parts = data.split("_", 3)
        level_key = parts[1]
        scholar_id = int(parts[2])
        info_field_key_safe = parts[3]
        info_field = info_field_key_safe.replace('_', ':').replace('`', ' ') 
        
        scholar_data = scholars_data.get(level_key, {}).get(scholar_id, {})
        content = scholar_data.get(info_field, "لا يوجد محتوى لهذا الحقل.")
        
        # زر العودة لقائمة حقول العالم
        back_data = f"SCHOLAR_{level_key}_{scholar_id}"
        scholar_name = scholar_data.get("اسم_العالم", "العالم")
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔙 العودة لقائمة حقول {scholar_name}", callback_data=back_data)]
        ])
        
        text = f"**{scholar_name}**\n\n***{info_field}***\n\n{content}"
        
        # معالجة الرسائل الطويلة
        if len(text) > 4096:
            text = text[:4000] + "\n\n...(تم اختصار المحتوى بسبب طوله)..."

        try:
             await query.edit_message_text(text=text, reply_markup=back_keyboard, parse_mode='Markdown')
        except Exception:
             # إذا فشل التعديل (بسبب رسالة طويلة)، نرسل رسالة جديدة ونحذف لوحة المفاتيح القديمة
             await context.bot.send_message(
                 chat_id=chat_id,
                 text=text,
                 reply_markup=back_keyboard,
                 parse_mode='Markdown'
             )
             try:
                 await query.edit_message_reply_markup(reply_markup=None)
             except:
                 pass
        return

# =================================================================
# دالة التشغيل الرئيسية (Main Function)
# =================================================================
def main() -> None:
    """دالة التشغيل الرئيسية للبوت."""
    
    if not BOT_TOKEN or BOT_TOKEN == "ضع مفتاح البوت السري هنا":
        print("❌ خطأ: المفتاح غير صحيح أو فارغ.") 
        return

    # 1. بناء التطبيق (Application Builder)
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 2. إضافة معالجات الأوامر (Handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # 3. تشغيل البوت (Start Polling)
    print("🤖 البوت قيد التشغيل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()