from flask import Flask, render_template, request, jsonify
import pymysql
import os
from ai import ask_ai

app = Flask(__name__, template_folder='templates')
last_request = {}



print("Static folder:", app.static_folder)
print("Template folder:", app.template_folder)


db = pymysql.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT")),
    charset="utf8mb4"
)


cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")



# ==========================
# صفحة الأسئلة الشائعة
# ==========================

@app.route("/faq")
def faq():

    cursor.execute("SELECT question, answer FROM faq")
    data = cursor.fetchall()

    result = ""

    for row in data:

        result += f"<b>السؤال:</b> {row[0]}<br>"
        result += f"<b>الجواب:</b> {row[1]}<br><br>"

    return result


# ==========================
# صفحة التخصصات
# ==========================

@app.route("/majors")
def majors():

    cursor.execute("SELECT name, description, admission_grade FROM majors")

    majors = cursor.fetchall()

    return render_template("majors.html", majors=majors)






# ==========================
# صفحة الرسوم
# ==========================

@app.route("/fees")
def fees():

    cursor.execute("SELECT major, fee FROM fees")

    fees = cursor.fetchall()

    return render_template("fees.html", fees=fees)


# ==========================
# صفحة شروط القبول
# ==========================

@app.route("/admissions")
def admissions():

    cursor.execute("SELECT requirement FROM admissions")

    admissions = cursor.fetchall()

    return render_template("admissions.html", admissions=admissions)



# ==========================
# صفحة التسجيل 
# ==========================

@app.route("/registration")
def registration():
    return render_template("registration.html")




# ==========================
# الشات بوت
# ==========================

@app.route("/chat", methods=["GET", "POST"])
def chat():

    print("دخل الى الشات")

    answer = ""

    if request.method == "POST":

        question = request.form["question"].strip().lower()
        user = "default"



        # ==========================
        # الترحيب
        # ==========================

        if any(word in question for word in [
            "مرحبا",
            "مرحباً",
            "السلام عليكم",
            "اهلا",
            "أهلا",
            "هاي",
            "hello",
            "hi"
        ]):

            answer = "👋 أهلاً بك في شات بوت الجامعة الافتراضية السورية، كيف يمكنني مساعدتك؟"


        # ==========================
        # من أنت
        # ==========================

        elif any(word in question for word in [
            "من أنت",
            "من انت",
            "مين انت"
        ]):

            answer = (
                "🎓 أنا المساعد الذكي للجامعة الافتراضية السورية.\n\n"
                "أستطيع مساعدتك في:\n"
                "• التخصصات\n"
                "• الرسوم الدراسية\n"
                "• معدلات القبول\n"
                "• معلومات التخصصات\n"
                "• شروط القبول\n"
                "• مواعيد التسجيل"
            )


        # ==========================
        # الشكر
        # ==========================

        elif any(word in question for word in [
            "شكرا",
            "شكراً",
            "يسلمو",
            "يعطيك العافية"
        ]):

            answer = "😊 على الرحب والسعة، أتمنى لك التوفيق."


        # ==========================
        # عرض التخصصات
        # ==========================

        elif any(word in question for word in [
            "تخصص",
            "التخصصات",
            "شو في تخصصات",
            "ما هي التخصصات"
        ]):

            cursor.execute("SELECT name FROM majors")
            data = cursor.fetchall()

            answer = "📚 التخصصات المتوفرة:\n\n"

            for row in data:
                answer += f"• {row[0]}\n"


        # ==========================
        # الرسوم الدراسية
        # ==========================

        elif any(word in question for word in [
            "رسوم",
            "تكلفة",
            "قسط",
            "الأقساط",
            "قديش",
            "كم"
        ]):

            major_name = None

            if "الهندسة المعلوماتية" in question:
                major_name = "الهندسة المعلوماتية"

            elif "تقانة المعلومات" in question:
                major_name = "الإجازة في تقانة المعلومات"

            elif "تقانة الاتصالات" in question:
                major_name = "الإجازة في تقانة الاتصالات"

            elif "علوم الإدارة" in question:
                major_name = "الإجازة في علوم الإدارة"

            elif "الحقوق" in question:
                major_name = "الإجازة في الحقوق"

            elif "الإعلام" in question:
                major_name = "الإجازة في الإعلام والاتصال"

            elif "السياحية" in question or "الفندقية" in question:
                major_name = "الإجازة في الإدارة السياحية والفندقية"

            elif "الموارد البشرية" in question:
                major_name = "الإجازة في إدارة الموارد البشرية"

            elif "المعهد التقاني للحاسوب" in question:
                major_name = "المعهد التقاني للحاسوب"

            elif "المعهد التقاني لإدارة الأعمال" in question:
                major_name = "المعهد التقاني لإدارة الأعمال"

            elif "الإدارة الهندسية" in question or "الرقمنة" in question:
                major_name = "المعهد التقاني للإدارة الهندسية والرقمنة"

            if major_name:

                cursor.execute(
                    "SELECT fee FROM fees WHERE major=%s",
                    (major_name,)
                )

                fee = cursor.fetchone()

                if fee:
                    answer = f"💰 رسوم {major_name} هي: {fee[0]}"
                else:
                    answer = "❌ لا توجد رسوم مسجلة لهذا التخصص."

            else:
               last_request[user] = "fees"
               answer = "✍️ يرجى كتابة اسم التخصص لمعرفة الرسوم."

        # ==========================
        # معدلات القبول
        # ==========================

        elif "معدل" in question:

            major_name = None

            if "الهندسة المعلوماتية" in question:
                major_name = "الهندسة المعلوماتية"

            elif "تقانة المعلومات" in question:
                major_name = "الإجازة في تقانة المعلومات"

            elif "تقانة الاتصالات" in question:
                major_name = "الإجازة في تقانة الاتصالات"

            elif "علوم الإدارة" in question:
                major_name = "الإجازة في علوم الإدارة"

            elif "الحقوق" in question:
                major_name = "الإجازة في الحقوق"

            elif "الإعلام" in question:
                major_name = "الإجازة في الإعلام والاتصال"

            elif "السياحية" in question or "الفندقية" in question:
                major_name = "الإجازة في الإدارة السياحية والفندقية"

            elif "الموارد البشرية" in question:
                major_name = "الإجازة في إدارة الموارد البشرية"

            elif "المعهد التقاني للحاسوب" in question:
                major_name = "المعهد التقاني للحاسوب"

            elif "المعهد التقاني لإدارة الأعمال" in question:
                major_name = "المعهد التقاني لإدارة الأعمال"

            elif "الإدارة الهندسية" in question or "الرقمنة" in question:
                major_name = "المعهد التقاني للإدارة الهندسية والرقمنة"

            if major_name:

                cursor.execute(
                    "SELECT admission_grade FROM majors WHERE name=%s",
                    (major_name,)
                )

                grade = cursor.fetchone()

                if grade:
                    answer = f"🎓 معدل القبول في {major_name} هو: {grade[0]}"
                else:
                    answer = "لا يوجد معدل قبول لهذا التخصص."

            else:
                answer = "✍️ يرجى كتابة اسم التخصص."


        # ==========================
        # معلومات التخصص
        # ==========================

        elif any(word in question for word in [
            "معلومات",
            "نبذة",
            "وصف"
        ]):

            major_name = None

            if "الهندسة المعلوماتية" in question:
                major_name = "الهندسة المعلوماتية"

            elif "تقانة المعلومات" in question:
                major_name = "الإجازة في تقانة المعلومات"

            elif "تقانة الاتصالات" in question:
                major_name = "الإجازة في تقانة الاتصالات"

            elif "علوم الإدارة" in question:
                major_name = "الإجازة في علوم الإدارة"

            elif "الحقوق" in question:
                major_name = "الإجازة في الحقوق"

            elif "الإعلام" in question:
                major_name = "الإجازة في الإعلام والاتصال"

            elif "السياحية" in question or "الفندقية" in question:
                major_name = "الإجازة في الإدارة السياحية والفندقية"

            elif "الموارد البشرية" in question:
                major_name = "الإجازة في إدارة الموارد البشرية"

            elif "المعهد التقاني للحاسوب" in question:
                major_name = "المعهد التقاني للحاسوب"

            elif "المعهد التقاني لإدارة الأعمال" in question:
                major_name = "المعهد التقاني لإدارة الأعمال"

            elif "الإدارة الهندسية" in question or "الرقمنة" in question:
                major_name = "المعهد التقاني للإدارة الهندسية والرقمنة"

            if major_name:

                cursor.execute(
                    "SELECT description FROM majors WHERE name=%s",
                    (major_name,)
                )

                info = cursor.fetchone()

                if info:
                    answer = info[0]
                else:
                    answer = "لا توجد معلومات لهذا التخصص."

            else:
                answer = "✍️ يرجى كتابة اسم التخصص."

        # ==========================
        # شروط القبول
        # ==========================

        elif any(word in question for word in [
            "قبول",
            "شروط القبول",
            "كيف انقبل"
        ]):

            cursor.execute("SELECT requirement FROM admissions")
            data = cursor.fetchall()

            answer = "📄 شروط القبول:\n\n"

            for row in data:
                answer += f"• {row[0]}\n"


        # ==========================
        # التسجيل
        # ==========================

        elif any(word in question for word in [
            "تسجيل",
            "موعد التسجيل",
            "متى يبدأ التسجيل"
        ]):

            cursor.execute(
                "SELECT answer FROM faq WHERE question=%s",
                ("متى يبدأ التسجيل؟",)
            )

            data = cursor.fetchone()

            if data:
                answer = data[0]
            else:
                answer = "لا توجد معلومات عن التسجيل."


        # ==========================
        # متابعة آخر طلب
        # ==========================

        elif user in last_request:

            if last_request[user] == "fees":

                major_name = None

                if "الهندسة المعلوماتية" in question:
                    major_name = "الهندسة المعلوماتية"

                elif "تقانة المعلومات" in question:
                    major_name = "الإجازة في تقانة المعلومات"

                elif "تقانة الاتصالات" in question:
                    major_name = "الإجازة في تقانة الاتصالات"

                elif "علوم الإدارة" in question:
                    major_name = "الإجازة في علوم الإدارة"

                elif "الحقوق" in question:
                    major_name = "الإجازة في الحقوق"

                elif "الإعلام" in question:
                    major_name = "الإجازة في الإعلام والاتصال"

                elif "السياحية" in question or "الفندقية" in question:
                    major_name = "الإجازة في الإدارة السياحية والفندقية"

                elif "الموارد البشرية" in question:
                    major_name = "الإجازة في إدارة الموارد البشرية"

                elif "المعهد التقاني للحاسوب" in question:
                    major_name = "المعهد التقاني للحاسوب"

                elif "المعهد التقاني لإدارة الأعمال" in question:
                    major_name = "المعهد التقاني لإدارة الأعمال"

                elif "الإدارة الهندسية" in question or "الرقمنة" in question:
                    major_name = "المعهد التقاني للإدارة الهندسية والرقمنة"

                if major_name:

                    cursor.execute(
                        "SELECT fee FROM fees WHERE major=%s",
                        (major_name,)
                    )

                    fee = cursor.fetchone()

                    if fee:
                        answer = f"💰 رسوم {major_name} هي: {fee[0]}"

                    del last_request[user]



        # ==========================
        # الذكاء الصناعي
        # ==========================

        else:

            ai_answer = ask_ai(question)

            if ai_answer:
                answer = ai_answer
            else:
                answer = "🤖 عذرًا، لا أستطيع الإجابة عن هذا السؤال حاليًا."


        # ==========================
        # حفظ المحادثة
        # ==========================

        cursor.execute(
            """
            INSERT INTO chat_history(question, answer)
            VALUES (%s, %s)
            """,
            (question, answer)
        )

        db.commit()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"answer": answer})

    return render_template("chat.html", answer=answer)


# ==========================
# تشغيل التطبيق
# ==========================

import os
print(os.getcwd())

if __name__ == "__main__":
    app.run(debug=True)

# ==========================
# 
# ==========================








