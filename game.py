import streamlit as st
import random

# إعدادات الصفحة
st.set_page_config(page_title="عالم المغامرات المفتوح", page_icon="⚔️", layout="centered")

st.title("⚔️ عالم المغامرات المفتوح (RPG)")
st.write("مرحباً بكِ في عالم السحر والمغامرة! تنقلي بين المناطق، اجمعي الذهب، وحاربي الأعداء لتصبحي أقوى محاربة.")

# --- تهيئة بيانات اللاعب في الجلسة ---
if "player" not in st.session_state:
    st.session_state.player = {
        "level": 1,
        "hp": 100,
        "max_hp": 100,
        "gold": 50,
        "attack": 15,
        "location": "المدينة الرئيسية 🏙️",
        "inventory": ["سيف خشبي 🗡️"],
        "logs": ["بدأتِ مغامرتكِ الآن في المدينة الافتراضية!"]
    }

p = st.session_state.player

# --- لوحة تحكم معلومات اللاعب ---
st.sidebar.header("👤 ملف المحاربة")
st.sidebar.write(f"**المستوى:** {p['level']}")
st.sidebar.write(f"**الصحة (HP):** {p['hp']}/{p['max_hp']}")
st.sidebar.write(f"**الذهب 💰:** {p['gold']}")
st.sidebar.write(f"**قوة الهجوم ⚔️:** {p['attack']}")
st.sidebar.write(f"**الموقع الحالي:** {p['location']}")
st.sidebar.write(f"**الحقيبة 🎒:** {', '.join(p['inventory'])}")

if st.sidebar.button("إعادة بدء اللعبة 🔄"):
    del st.session_state.player
    st.rerun()

# --- خريطة العالم والتنقل ---
st.subheader("🗺️ أين تريدين الذهاب الآن؟")
locations = ["المدينة الرئيسية 🏙️", "الغابة المظلمة 🌲", "القلعة المهجورة 🏰", "السوق المحلي 🏪"]

# اختيار المكان عبر أزرار
col_locs = st.columns(4)
for i, loc in enumerate(locations):
    with col_locs[i]:
        if st.button(loc, key=f"btn_{loc}"):
            p["location"] = loc
            p["logs"].append(f"سافرتِ إلى {loc}.")
            st.rerun()

st.markdown("---")

# --- أحداث المناطق ---
st.subheader(f"📍 أحداث: {p['location']}")

# 1. أحداث المدينة
if p["location"] == "المدينة الرئيسية 🏙️":
    st.write("المكان هنا آمن تماماً. يمكنكِ الاستراحة هنا لاستعادة صحتكِ بالكامل مجاناً!")
    if st.button("🛏️ استراحة في الفندق (استعادة الصحة)"):
        p["hp"] = p["max_hp"]
        p["logs"].append("نمتِ في الفندق واستعدتِ صحتكِ بالكامل.")
        st.success("تمت استعادة الصحة 100%!")
        st.rerun()

# 2. أحداث الغابة المظلمة (قتال أو جمع ذهب)
elif p["location"] == "الغابة المظلمة 🌲":
    st.write("احترسي! الغابة مليئة بالوحوش الصغيرة والنباتات السحرية.")
    
    col_forest = st.columns(2)
    with col_forest[0]:
        if st.button("🔍 البحث عن أعشاب سحرية (بحث عن ذهب)"):
            found_gold = random.randint(10, 30)
            p["gold"] += found_gold
            p["logs"].append(f"وجدتِ أعشاباً نادرة وبعتِها بـ {found_gold} قطعة ذهبية.")
            st.success(f"وجدتي {found_gold} ذهب!")
            st.rerun()
            
    with col_forest[1]:
        if st.button("⚔️ محاربة ذئب الغابة"):
            damage_taken = random.randint(10, 25)
            gold_won = random.randint(20, 50)
            p["hp"] -= damage_taken
            if p["hp"] <= 0:
                p["hp"] = 0
                p["logs"].append("هزمكِ ذئب الغابة! عودي للمدينة للاستراحة.")
                st.error("لقد هُزمتِ في المعركة! صحتكِ أصبحت 0.")
            else:
                p["gold"] += gold_won
                p["logs"].append(f"هزمتِ الذئب! خسرتِ {damage_taken} HP وربحتِ {gold_won} ذهب.")
                st.success(f"انتصار! ربحتِ {gold_won} ذهب وتلقيتِ {damage_taken} ضرر.")
            st.rerun()

# 3. أحداث القلعة المهجورة (زعيم قوي ومكافأة كبرى)
elif p["location"] == "القلعة المهجورة 🏰":
    st.write("هنا يسكن التنين الصغير المحرس للكنز الأسطوري! القتال هنا صعب جداً.")
    if st.button("🐉 مواجهة التنين الأسطوري"):
        if p["attack"] < 25:
            st.warning("هجومكِ ضعيف جداً! اذهبي للسوق واشتري سيفاً أقوى أولاً.")
        else:
            damage_taken = random.randint(30, 60)
            p["hp"] -= damage_taken
            if p["hp"] <= 0:
                p["hp"] = 0
                p["logs"].append("سحقكِ التنين! تحتاجين لقوة أكبر وصفاء ذهني.")
                st.error("هزيمة ساحقة من التنين!")
            else:
                p["gold"] += 200
                p["level"] += 1
                p["logs"].append(f"هزمتِ التنين الأسطوري! ارتفع مستواكِ وكسبتِ 200 ذهب!")
                st.balloons()
                st.success("🎉 إنجاز أسطوري! هزمتِ التنين وارتفع مستواكِ!")
            st.rerun()

# 4. أحداث السوق المحلي
elif p["location"] == "السوق المحلي 🏪":
    st.write("مرحباً بكِ في الدكان، يمكنكِ تطوير سلاحكِ لزيادة قوتكِ الهجومية.")
    st.write(f"سعر السيف الفولاذي المطور: **60 قطعة ذهبية** (+15 قوة هجوم)")
    
    if "سيف فولاذي ⚔️" in p["inventory"]:
        st.info("لقد اشتريتِ أفضل سيف متوفر بالفعل!")
    else:
        if st.button("💰 شراء سيف فولاذي"):
            if p["gold"] >= 60:
                p["gold"] -= 60
                p["attack"] += 15
                p["inventory"].append("سيف فولاذي ⚔️")
                p["logs"].append("اشتريتِ سيفاً فولاذياً مطوراً من السوق.")
                st.success("مبروك السلاح الجديد!")
                st.rerun()
            else:
                st.error("لا تملكين الذهب الكافي!")

st.markdown("---")

# --- سجل الأحداث المتجدد ---
st.subheader("📜 سجل المغامرة (ماذا حدث؟)")
for log in reversed(p["logs"][-5:]): # عرض آخر 5 أحداث فقط
    st.write(f"- {log}")
