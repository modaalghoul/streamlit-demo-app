"""
تطبيق إدارة الأدوية - النسخة التجريبية (Prototype)
Drug Management System - Prototype Version

تطبيق ويب تفاعلي لعرض واستكشاف بيانات الأدوية
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# ===================================================================
# إعدادات الصفحة
# ===================================================================
st.set_page_config(
    page_title="نظام إدارة الأدوية",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================================================
# الاتصال بقاعدة البيانات
# ===================================================================
DB_PATH = "drug_database.db"

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """تهيئة قاعدة البيانات إذا لم تكن موجودة"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        with open('database_schema.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        return True
    return False

# ===================================================================
# دوال قاعدة البيانات
# ===================================================================

def get_all_medications():
    """جلب جميع الأدوية مع المعلومات الكاملة"""
    conn = get_db_connection()
    query = """
    SELECT 
        m.*,
        c.name_ar as category_name,
        dt.name_ar as drug_type_name,
        mf.name as manufacturer_name
    FROM medications m
    LEFT JOIN categories c ON m.category_id = c.id
    LEFT JOIN drug_types dt ON m.drug_type_id = dt.id
    LEFT JOIN manufacturers mf ON m.manufacturer_id = mf.id
    ORDER BY m.id DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_categories():
    """جلب جميع الفئات"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM categories", conn)
    conn.close()
    return df

def get_drug_types():
    """جلب جميع أنواع الأدوية"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM drug_types", conn)
    conn.close()
    return df

def get_manufacturers():
    """جلب جميع الشركات المصنعة"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM manufacturers", conn)
    conn.close()
    return df

def get_age_weight_estimates():
    """جلب تقديرات الأوزان حسب العمر"""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM age_weight_estimates ORDER BY age_months", conn)
    conn.close()
    return df

def add_medication(data):
    """إضافة دواء جديد"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    query = f"INSERT INTO medications ({columns}) VALUES ({placeholders})"
    
    cursor.execute(query, list(data.values()))
    conn.commit()
    conn.close()
    return True

def add_manufacturer(name, name_ar, country):
    """إضافة شركة مصنعة جديدة"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO manufacturers (name, name_ar, country) VALUES (?, ?, ?)",
        (name, name_ar, country)
    )
    conn.commit()
    conn.close()
    return True

def add_category(name, name_ar, description=""):
    """إضافة فئة جديدة"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (name, name_ar, description) VALUES (?, ?, ?)",
        (name, name_ar, description)
    )
    conn.commit()
    conn.close()
    return True

def add_drug_type(name, name_ar, description=""):
    """إضافة نوع دواء جديد"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO drug_types (name, name_ar, description) VALUES (?, ?, ?)",
        (name, name_ar, description)
    )
    conn.commit()
    conn.close()
    return True

def update_medication(medication_id, data):
    """تحديث بيانات دواء"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
    query = f"UPDATE medications SET {set_clause} WHERE id = ?"
    
    cursor.execute(query, list(data.values()) + [medication_id])
    conn.commit()
    conn.close()
    return True

def delete_medication(medication_id):
    """حذف دواء"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medications WHERE id = ?", (medication_id,))
    conn.commit()
    conn.close()
    return True

def delete_category(category_id):
    """حذف فئة"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()
    return True

def delete_drug_type(drug_type_id):
    """حذف نوع دواء"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drug_types WHERE id = ?", (drug_type_id,))
    conn.commit()
    conn.close()
    return True

def delete_manufacturer(manufacturer_id):
    """حذف شركة مصنعة"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM manufacturers WHERE id = ?", (manufacturer_id,))
    conn.commit()
    conn.close()
    return True

# ===================================================================
# واجهة المستخدم الرئيسية
# ===================================================================

def main():
    # تهيئة قاعدة البيانات
    if init_database():
        st.success("✅ تم إنشاء قاعدة البيانات بنجاح!")
    
    # العنوان الرئيسي
    st.title("💊 نظام إدارة الأدوية")
    st.markdown("---")
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("📋 القائمة الرئيسية")
        page = st.radio(
            "اختر الصفحة:",
            ["🏠 الصفحة الرئيسية", 
             "💊 عرض الأدوية", 
             "➕ إضافة دواء جديد",
             "🏭 إدارة الشركات المصنعة",
             "📂 إدارة الفئات",
             "🔢 إدارة أنواع الأدوية",
             "📊 تقديرات الأوزان",
             "📈 الإحصائيات",
             "📥 استيراد من Excel"]
        )
        
        st.markdown("---")
        st.info("**ملاحظة:** هذا تطبيق تجريبي لاستكشاف البيانات واختبار السيناريوهات")
    
    # عرض الصفحات حسب الاختيار
    if page == "🏠 الصفحة الرئيسية":
        show_home_page()
    elif page == "💊 عرض الأدوية":
        show_medications_page()
    elif page == "➕ إضافة دواء جديد":
        show_add_medication_page()
    elif page == "🏭 إدارة الشركات المصنعة":
        show_manufacturers_page()
    elif page == "📂 إدارة الفئات":
        show_categories_page()
    elif page == "🔢 إدارة أنواع الأدوية":
        show_drug_types_page()
    elif page == "📊 تقديرات الأوزان":
        show_weight_estimates_page()
    elif page == "📈 الإحصائيات":
        show_statistics_page()
    elif page == "📥 استيراد من Excel":
        show_import_page()

# ===================================================================
# صفحة الرئيسية
# ===================================================================
def show_home_page():
    st.header("🏠 الصفحة الرئيسية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    meds_df = get_all_medications()
    cats_df = get_categories()
    types_df = get_drug_types()
    manufacturers_df = get_manufacturers()
    
    with col1:
        st.metric("💊 إجمالي الأدوية", len(meds_df))
    with col2:
        st.metric("📂 الفئات", len(cats_df))
    with col3:
        st.metric("🏭 الشركات المصنعة", len(manufacturers_df))
    with col4:
        st.metric("🔢 أنواع الأدوية", len(types_df))
    
    st.markdown("---")
    
    st.subheader("📋 نظرة عامة على قاعدة البيانات")
    
    tab1, tab2, tab3 = st.tabs(["الفئات", "أنواع الأدوية", "الشركات المصنعة"])
    
    with tab1:
        st.dataframe(cats_df, use_container_width=True)
    
    with tab2:
        st.dataframe(types_df, use_container_width=True)
    
    with tab3:
        st.dataframe(manufacturers_df, use_container_width=True)

# ===================================================================
# صفحة عرض الأدوية
# ===================================================================
def show_medications_page():
    st.header("💊 عرض الأدوية")
    
    # البحث والتصفية
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 بحث بالاسم العلمي أو التجاري")
    
    with col2:
        categories = get_categories()
        selected_category = st.selectbox(
            "تصفية حسب الفئة",
            ["الكل"] + categories['name_ar'].tolist()
        )
    
    with col3:
        availability_filter = st.selectbox(
            "تصفية حسب التوفر",
            ["الكل", "متوفر", "غير متوفر"]
        )
    
    # جلب البيانات
    df = get_all_medications()
    
    # تطبيق الفلاتر
    if search_term:
        df = df[
            df['generic_name'].str.contains(search_term, case=False, na=False) | 
            df['trade_name'].str.contains(search_term, case=False, na=False)
        ]
    
    if selected_category != "الكل":
        df = df[df['category_name'] == selected_category]
    
    if availability_filter != "الكل":
        df = df[df['availability'] == availability_filter]
    
    st.info(f"📊 عدد الأدوية المعروضة: {len(df)}")
    
    # عرض البيانات
    if len(df) > 0:
        # اختيار الأعمدة للعرض
        display_columns = [
            'id', 'generic_name', 'trade_name', 'category_display', 
            'concentration', 'form', 'manufacturer_name', 'price', 'availability'
        ]
        
        # إعادة تسمية الأعمدة للعربية وتنسيق الفئة
        # إضافة عمود مدمج للفئة
        if 'category_name' in df.columns and 'category_id' in df.columns:
            cats_df = get_categories()
            df['category_display'] = df.apply(
                lambda row: f"{cats_df[cats_df['id']==row['category_id']]['name'].values[0]} ({row['category_name']})" 
                if pd.notna(row['category_name']) and len(cats_df[cats_df['id']==row['category_id']]) > 0
                else row['category_name'] if pd.notna(row['category_name']) else '-',
                axis=1
            )
        
        column_names = {
            'id': 'المعرف',
            'generic_name': 'الاسم العلمي',
            'trade_name': 'الاسم التجاري',
            'category_display': 'الفئة',
            'concentration': 'التركيز',
            'form': 'الشكل',
            'manufacturer_name': 'الشركة',
            'price': 'السعر',
            'availability': 'التوفر'
        }
        
        display_df = df[display_columns].rename(columns=column_names)
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # عرض تفاصيل دواء محدد
        st.markdown("---")
        st.subheader("📋 تفاصيل الدواء")
        
        selected_id = st.selectbox(
            "اختر دواء لعرض التفاصيل",
            df['id'].tolist(),
            format_func=lambda x: f"{df[df['id']==x]['trade_name'].values[0]} - {df[df['id']==x]['generic_name'].values[0]}"
        )
        
        if selected_id:
            show_medication_details(df[df['id'] == selected_id].iloc[0])
    else:
        st.warning("⚠️ لا توجد بيانات للعرض")

def show_medication_details(medication):
    """عرض تفاصيل دواء معين"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📌 المعلومات الأساسية")
        st.write(f"**الاسم العلمي:** {medication['generic_name']}")
        st.write(f"**الاسم التجاري:** {medication['trade_name']}")
        
        # عرض الفئة بالاسمين
        categories = get_categories()
        if pd.notna(medication.get('category_id')) and len(categories[categories['id']==medication['category_id']]) > 0:
            cat_row = categories[categories['id']==medication['category_id']].iloc[0]
            cat_display = f"{cat_row['name']} ({cat_row['name_ar']})" if pd.notna(cat_row['name_ar']) else cat_row['name']
            st.write(f"**الفئة:** {cat_display}")
        else:
            st.write(f"**الفئة:** {medication['category_name']}")
        
        # عرض نوع الدواء بالاسمين
        drug_types = get_drug_types()
        if pd.notna(medication.get('drug_type_id')) and len(drug_types[drug_types['id']==medication['drug_type_id']]) > 0:
            type_row = drug_types[drug_types['id']==medication['drug_type_id']].iloc[0]
            type_display = f"{type_row['name']} ({type_row['name_ar']})" if pd.notna(type_row['name_ar']) else type_row['name']
            st.write(f"**النوع:** {type_display}")
        elif pd.notna(medication.get('drug_type_name')):
            st.write(f"**النوع:** {medication['drug_type_name']}")
        
        # عرض الشركة بالاسمين
        manufacturers = get_manufacturers()
        if pd.notna(medication.get('manufacturer_id')) and len(manufacturers[manufacturers['id']==medication['manufacturer_id']]) > 0:
            mfr_row = manufacturers[manufacturers['id']==medication['manufacturer_id']].iloc[0]
            mfr_display = f"{mfr_row['name']} ({mfr_row['name_ar']})" if pd.notna(mfr_row['name_ar']) else mfr_row['name']
            st.write(f"**الشركة المصنعة:** {mfr_display}")
        else:
            st.write(f"**الشركة المصنعة:** {medication['manufacturer_name']}")
        
        st.write(f"**التركيز:** {medication['concentration']}")
        st.write(f"**الشكل الصيدلاني:** {medication['form']}")
    
    with col2:
        st.markdown("### 💰 المعلومات التجارية")
        st.write(f"**السعر:** {medication['price']} دينار" if pd.notna(medication['price']) else "غير محدد")
        st.write(f"**السعر مع الضريبة:** {medication['price_with_tax']} دينار" if pd.notna(medication['price_with_tax']) else "غير محدد")
        st.write(f"**التوفر:** {medication['availability']}" if pd.notna(medication['availability']) else "غير محدد")
        st.write(f"**التعبئة:** {medication['package_info']}" if pd.notna(medication['package_info']) else "غير محدد")
        st.write(f"**بلد التصنيع:** {medication['manufacturing_country']}" if pd.notna(medication['manufacturing_country']) else "غير محدد")
    
    st.markdown("---")
    
    with st.expander("💊 معلومات الجرعة"):
        st.write(f"**الحد العمري:** {medication['age_limit_text']}" if pd.notna(medication['age_limit_text']) else "غير محدد")
        st.write(f"**الحد الوزني:** {medication['weight_limit_text']}" if pd.notna(medication['weight_limit_text']) else "غير محدد")
        st.write(f"**الجرعة القصوى للجرعة الواحدة:** {medication['max_single_dose']}" if pd.notna(medication['max_single_dose']) else "غير محدد")
        st.write(f"**معادلة حساب الجرعة:** {medication['dose_calculation']}" if pd.notna(medication['dose_calculation']) else "غير محدد")
        st.write(f"**الجرعة القصوى اليومية:** {medication['max_daily_dose']}" if pd.notna(medication['max_daily_dose']) else "غير محدد")
        st.write(f"**التكرار:** {medication['frequency']}" if pd.notna(medication['frequency']) else "غير محدد")
    
    with st.expander("⚠️ محاذير الاستخدام والتحذيرات"):
        st.write(f"**دواعي الاستعمال:** {medication['indications']}" if pd.notna(medication['indications']) else "غير محدد")
        st.write(f"**محاذير الاستخدام:** {medication['contraindications']}" if pd.notna(medication['contraindications']) else "غير محدد")
        st.write(f"**الآثار الجانبية:** {medication['side_effects']}" if pd.notna(medication['side_effects']) else "غير محدد")
        st.write(f"**التفاعلات الدوائية:** {medication['drug_interactions']}" if pd.notna(medication['drug_interactions']) else "غير محدد")
        st.write(f"**تحذيرات:** {medication['warnings']}" if pd.notna(medication['warnings']) else "غير محدد")
    
    with st.expander("🤰 الحمل والرضاعة"):
        st.write(f"**فئة الحمل:** {medication['pregnancy_category']}" if pd.notna(medication['pregnancy_category']) else "غير محدد")
        st.write(f"**الأمان أثناء الحمل:** {medication['pregnancy_safety']}" if pd.notna(medication['pregnancy_safety']) else "غير محدد")
        st.write(f"**الأمان أثناء الرضاعة:** {medication['lactation_safety']}" if pd.notna(medication['lactation_safety']) else "غير محدد")
    
    with st.expander("📦 التخزين"):
        st.write(f"**ظروف التخزين:** {medication['storage_conditions']}" if pd.notna(medication['storage_conditions']) else "غير محدد")
        st.write(f"**مدة الصلاحية:** {medication['shelf_life']}" if pd.notna(medication['shelf_life']) else "غير محدد")

# ===================================================================
# صفحة إضافة دواء جديد
# ===================================================================
def show_add_medication_page():
    st.header("➕ إضافة دواء جديد")
    
    with st.form("add_medication_form"):
        st.subheader("📌 المعلومات الأساسية")
        
        col1, col2 = st.columns(2)
        with col1:
            generic_name = st.text_input("الاسم العلمي *", placeholder="مثال: paracetamol")
            trade_name = st.text_input("الاسم التجاري", placeholder="مثال: Adol")
            
            categories = get_categories()
            category_id = st.selectbox(
                "الفئة",
                options=categories['id'].tolist(),
                format_func=lambda x: f"{categories[categories['id']==x]['name'].values[0]} ({categories[categories['id']==x]['name_ar'].values[0]})" if pd.notna(categories[categories['id']==x]['name_ar'].values[0]) else categories[categories['id']==x]['name'].values[0]
            )
        
        with col2:
            concentration = st.text_input("التركيز", placeholder="مثال: 100mg/1ml")
            form = st.selectbox(
                "الشكل الصيدلاني",
                ["oral drops", "suspension", "suppository", "tablet", "capsule", "syrup", "injection"]
            )
            
            manufacturers = get_manufacturers()
            if len(manufacturers) > 0:
                manufacturer_id = st.selectbox(
                    "الشركة المصنعة",
                    options=[None] + manufacturers['id'].tolist(),
                    format_func=lambda x: "غير محدد" if x is None else (
                        f"{manufacturers[manufacturers['id']==x]['name'].values[0]} ({manufacturers[manufacturers['id']==x]['name_ar'].values[0]})"
                        if pd.notna(manufacturers[manufacturers['id']==x]['name_ar'].values[0]) 
                        else manufacturers[manufacturers['id']==x]['name'].values[0]
                    )
                )
            else:
                manufacturer_id = None
                st.warning("لا توجد شركات مصنعة. يرجى إضافة شركة أولاً.")
        
        st.markdown("---")
        st.subheader("💊 معلومات الجرعة")
        
        col3, col4 = st.columns(2)
        with col3:
            age_limit_text = st.text_input("الحد العمري", placeholder="مثال: من شهر إلى 3 سنوات")
            weight_limit_text = st.text_input("الحد الوزني", placeholder="مثال: من 4.4 إلى 14.1 كجم")
        
        with col4:
            max_single_dose = st.text_input("الجرعة القصوى للجرعة الواحدة", placeholder="مثال: 2 ml")
            max_daily_dose = st.text_input("الجرعة القصوى اليومية", placeholder="مثال: 60mg/kg/day")
        
        dose_calculation = st.text_area("معادلة حساب الجرعة", placeholder="مثال: 10-15 mg/kg/dose every 6 hours")
        frequency = st.text_input("التكرار", placeholder="مثال: every 6 hours")
        
        st.markdown("---")
        st.subheader("💰 المعلومات التجارية")
        
        col5, col6 = st.columns(2)
        with col5:
            price = st.number_input("السعر (دينار)", min_value=0.0, step=0.1)
            availability = st.selectbox("التوفر", ["متوفر", "غير متوفر", "نادر"])
        
        with col6:
            package_info = st.text_input("التعبئة", placeholder="مثال: 15ml bottle")
            warehouse_name = st.text_input("اسم المستودع")
        
        st.markdown("---")
        st.subheader("⚠️ معلومات طبية إضافية (اختياري)")
        
        contraindications = st.text_area("محاذير الاستخدام")
        side_effects = st.text_area("الآثار الجانبية")
        warnings = st.text_area("تحذيرات")
        
        submitted = st.form_submit_button("حفظ الدواء", use_container_width=True, type="primary")
        
        if submitted:
            if not generic_name:
                st.error("❌ الرجاء إدخال الاسم العلمي على الأقل")
            else:
                medication_data = {
                    'generic_name': generic_name,
                    'trade_name': trade_name if trade_name else None,
                    'category_id': category_id,
                    'manufacturer_id': manufacturer_id,
                    'concentration': concentration if concentration else None,
                    'form': form,
                    'age_limit_text': age_limit_text if age_limit_text else None,
                    'weight_limit_text': weight_limit_text if weight_limit_text else None,
                    'max_single_dose': max_single_dose if max_single_dose else None,
                    'max_daily_dose': max_daily_dose if max_daily_dose else None,
                    'dose_calculation': dose_calculation if dose_calculation else None,
                    'frequency': frequency if frequency else None,
                    'price': price if price > 0 else None,
                    'availability': availability,
                    'package_info': package_info if package_info else None,
                    'warehouse_name': warehouse_name if warehouse_name else None,
                    'contraindications': contraindications if contraindications else None,
                    'side_effects': side_effects if side_effects else None,
                    'warnings': warnings if warnings else None,
                }
                
                try:
                    add_medication(medication_data)
                    st.success("✅ تم إضافة الدواء بنجاح!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")

# ===================================================================
# صفحة إدارة الشركات المصنعة
# ===================================================================
def show_manufacturers_page():
    st.header("🏭 إدارة الشركات المصنعة")
    
    # عرض الشركات الحالية
    manufacturers = get_manufacturers()
    st.subheader("📋 الشركات المصنعة الحالية")
    st.dataframe(manufacturers, use_container_width=True)
    
    st.markdown("---")
    
    # إضافة شركة جديدة
    st.subheader("➕ إضافة شركة مصنعة جديدة")
    
    with st.form("add_manufacturer_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("اسم الشركة (إنجليزي) *", placeholder="مثال: HIKMA")
        
        with col2:
            name_ar = st.text_input("اسم الشركة (عربي)", placeholder="مثال: حكمة")
        
        with col3:
            country = st.text_input("البلد", placeholder="مثال: Jordan")
        
        submitted = st.form_submit_button("إضافة الشركة", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ الرجاء إدخال اسم الشركة")
            else:
                try:
                    add_manufacturer(name, name_ar, country)
                    st.success(f"✅ تم إضافة شركة {name} بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")

# ===================================================================
# صفحة تقديرات الأوزان
# ===================================================================
def show_weight_estimates_page():
    st.header("📊 تقديرات الأوزان حسب العمر")
    
    df = get_age_weight_estimates()
    
    tab1, tab2, tab3 = st.tabs(["📅 0-11 شهر", "📅 1-5 سنوات", "📅 6-15 سنة"])
    
    with tab1:
        df_0_11 = df[df['age_group'] == '0-11 months']
        st.dataframe(df_0_11, use_container_width=True)
        st.line_chart(df_0_11.set_index('age_text')['estimated_weight_kg'])
    
    with tab2:
        df_1_5 = df[df['age_group'] == '1-5 years']
        st.dataframe(df_1_5, use_container_width=True)
        st.line_chart(df_1_5.set_index('age_text')['estimated_weight_kg'])
    
    with tab3:
        df_6_15 = df[df['age_group'] == '6-15 years']
        st.dataframe(df_6_15, use_container_width=True)
        st.line_chart(df_6_15.set_index('age_text')['estimated_weight_kg'])

# ===================================================================
# صفحة الإحصائيات
# ===================================================================
def show_statistics_page():
    st.header("📈 الإحصائيات")
    
    df = get_all_medications()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("توزيع الأدوية حسب الفئة")
        if len(df) > 0:
            category_counts = df['category_name'].value_counts()
            st.bar_chart(category_counts)
        else:
            st.info("لا توجد بيانات للعرض")
    
    with col2:
        st.subheader("توزيع الأدوية حسب الشكل الصيدلاني")
        if len(df) > 0:
            form_counts = df['form'].value_counts()
            st.bar_chart(form_counts)
        else:
            st.info("لا توجد بيانات للعرض")
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("توزيع الأدوية حسب الشركة المصنعة")
        if len(df) > 0:
            manufacturer_counts = df['manufacturer_name'].value_counts().head(10)
            st.bar_chart(manufacturer_counts)
        else:
            st.info("لا توجد بيانات للعرض")
    
    with col4:
        st.subheader("توزيع الأدوية حسب التوفر")
        if len(df) > 0:
            availability_counts = df['availability'].value_counts()
            st.bar_chart(availability_counts)
        else:
            st.info("لا توجد بيانات للعرض")

# ===================================================================
# صفحة إدارة الفئات
# ===================================================================
def show_categories_page():
    st.header("📂 إدارة الفئات")
    
    # عرض الفئات الحالية
    categories = get_categories()
    st.subheader("📋 الفئات الحالية")
    
    if len(categories) > 0:
        # عرض مع خيارات الحذف
        for idx, row in categories.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 1])
            with col1:
                st.write(f"**{row['id']}**")
            with col2:
                st.write(row['name'])
            with col3:
                st.write(row['name_ar'] if pd.notna(row['name_ar']) else "-")
            with col4:
                st.write(row['description'] if pd.notna(row['description']) else "-")
            with col5:
                if st.button("🗑️", key=f"del_cat_{row['id']}"):
                    try:
                        delete_category(row['id'])
                        st.success(f"✅ تم حذف الفئة")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
    else:
        st.info("لا توجد فئات")
    
    st.markdown("---")
    
    # إضافة فئة جديدة
    st.subheader("➕ إضافة فئة جديدة")
    
    with st.form("add_category_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("اسم الفئة (إنجليزي) *", placeholder="مثال: pediatric")
            name_ar = st.text_input("اسم الفئة (عربي)", placeholder="مثال: أطفال")
        
        with col2:
            description = st.text_area("الوصف (اختياري)", placeholder="وصف الفئة")
        
        submitted = st.form_submit_button("إضافة الفئة", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ الرجاء إدخال اسم الفئة")
            else:
                try:
                    add_category(name, name_ar, description)
                    st.success(f"✅ تم إضافة فئة {name} بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")

# ===================================================================
# صفحة إدارة أنواع الأدوية
# ===================================================================
def show_drug_types_page():
    st.header("🔢 إدارة أنواع الأدوية")
    
    # عرض الأنواع الحالية
    drug_types = get_drug_types()
    st.subheader("📋 أنواع الأدوية الحالية")
    
    if len(drug_types) > 0:
        # عرض مع خيارات الحذف
        for idx, row in drug_types.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 1])
            with col1:
                st.write(f"**{row['id']}**")
            with col2:
                st.write(row['name'])
            with col3:
                st.write(row['name_ar'] if pd.notna(row['name_ar']) else "-")
            with col4:
                st.write(row['description'] if pd.notna(row['description']) else "-")
            with col5:
                if st.button("🗑️", key=f"del_type_{row['id']}"):
                    try:
                        delete_drug_type(row['id'])
                        st.success(f"✅ تم حذف النوع")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
    else:
        st.info("لا توجد أنواع أدوية")
    
    st.markdown("---")
    
    # إضافة نوع جديد
    st.subheader("➕ إضافة نوع دواء جديد")
    
    with st.form("add_drug_type_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("اسم النوع (إنجليزي) *", placeholder="مثال: antibiotic")
            name_ar = st.text_input("اسم النوع (عربي)", placeholder="مثال: مضاد حيوي")
        
        with col2:
            description = st.text_area("الوصف (اختياري)", placeholder="وصف النوع")
        
        submitted = st.form_submit_button("إضافة النوع", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ الرجاء إدخال اسم النوع")
            else:
                try:
                    add_drug_type(name, name_ar, description)
                    st.success(f"✅ تم إضافة نوع {name} بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {str(e)}")

# ===================================================================
# صفحة استيراد من Excel
# ===================================================================
def show_import_page():
    st.header("📥 استيراد البيانات من Excel")
    
    st.info("""
    **ملاحظة:** هذه الميزة تسمح باستيراد البيانات من ملف Excel.
    
    يمكنك استيراد:
    - الأدوية
    - الشركات المصنعة
    - الفئات
    - أنواع الأدوية
    """)
    
    tab1, tab2 = st.tabs(["📤 رفع ملف", "📂 استيراد من الملف الموجود"])
    
    with tab1:
        st.subheader("رفع ملف Excel جديد")
        uploaded_file = st.file_uploader("اختر ملف Excel", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success(f"✅ تم قراءة الملف بنجاح! عدد الصفوف: {len(df)}")
                
                st.subheader("معاينة البيانات")
                st.dataframe(df.head(10))
                
                st.subheader("الأعمدة المتوفرة")
                st.write(df.columns.tolist())
                
                if st.button("استيراد البيانات", type="primary"):
                    st.warning("⚠️ هذه الميزة قيد التطوير...")
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
    
    with tab2:
        st.subheader("استيراد من ملف بيانات الأدوية الموجود")
        
        if os.path.exists('بيانات الادوية.xlsx'):
            if st.button("📥 استيراد من 'بيانات الادوية.xlsx'", type="primary"):
                with st.spinner("جاري الاستيراد..."):
                    try:
                        import_from_existing_excel()
                        st.success("✅ تم الاستيراد بنجاح!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ الملف 'بيانات الادوية.xlsx' غير موجود")
            
        st.markdown("---")
        st.subheader("إحصائيات سريعة")
        
        if os.path.exists('drug_data.csv'):
            df_csv = pd.read_csv('drug_data.csv', encoding='utf-8-sig')
            st.metric("عدد الصفوف في CSV", len(df_csv))
            
            if st.checkbox("عرض أول 20 صف"):
                st.dataframe(df_csv.head(20))

def import_from_existing_excel():
    """استيراد البيانات من ملف Excel الموجود"""
    # هذه دالة مبدئية - يمكن توسيعها لاحقًا
    st.info("🚧 هذه الميزة قيد التطوير...")
    st.write("""
    لاستيراد البيانات بشكل صحيح، يجب:
    1. تنظيف البيانات في Excel
    2. تحديد الأعمدة المقابلة لكل حقل
    3. معالجة القيم الفارغة
    4. التحقق من صحة البيانات
    """)

# ===================================================================
# تشغيل التطبيق
# ===================================================================
if __name__ == "__main__":
    main()
