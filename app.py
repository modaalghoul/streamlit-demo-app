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
             "🗄️ عرض قاعدة البيانات",
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
    elif page == "🗄️ عرض قاعدة البيانات":
        show_database_viewer_page()
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
        
        col_select, col_delete = st.columns([4, 1])
        
        with col_select:
            selected_id = st.selectbox(
                "اختر دواء لعرض التفاصيل",
                df['id'].tolist(),
                format_func=lambda x: f"{df[df['id']==x]['trade_name'].values[0]} - {df[df['id']==x]['generic_name'].values[0]}"
            )
        
        with col_delete:
            st.write("")
            st.write("")
            if st.button("🗑️ حذف الدواء", type="secondary", use_container_width=True):
                if st.session_state.get(f'confirm_delete_med_{selected_id}', False):
                    try:
                        delete_medication(selected_id)
                        st.success("✅ تم حذف الدواء بنجاح!")
                        st.session_state[f'confirm_delete_med_{selected_id}'] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
                else:
                    st.session_state[f'confirm_delete_med_{selected_id}'] = True
                    st.warning("⚠️ انقر مرة أخرى للتأكيد")
        
        if selected_id:
            show_medication_details(df[df['id'] == selected_id].iloc[0])
    else:
        st.warning("⚠️ لا توجد بيانات للعرض")

def show_medication_details(medication):
    """عرض تفاصيل دواء معين"""
    
    # المعلومات الأساسية
    with st.expander("📌 المعلومات الأساسية - Basic Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**الاسم العلمي:** {medication['generic_name']}")
            st.write(f"**الاسم التجاري:** {medication['trade_name']}" if pd.notna(medication['trade_name']) else "**الاسم التجاري:** غير محدد")
            
            # عرض الفئة بالاسمين
            categories = get_categories()
            if pd.notna(medication.get('category_id')) and len(categories[categories['id']==medication['category_id']]) > 0:
                cat_row = categories[categories['id']==medication['category_id']].iloc[0]
                cat_display = f"{cat_row['name']} ({cat_row['name_ar']})" if pd.notna(cat_row['name_ar']) else cat_row['name']
                st.write(f"**الفئة:** {cat_display}")
            else:
                st.write(f"**الفئة:** {medication['category_name']}" if pd.notna(medication.get('category_name')) else "**الفئة:** غير محدد")
            
            # عرض نوع الدواء بالاسمين
            drug_types = get_drug_types()
            if pd.notna(medication.get('drug_type_id')) and len(drug_types[drug_types['id']==medication['drug_type_id']]) > 0:
                type_row = drug_types[drug_types['id']==medication['drug_type_id']].iloc[0]
                type_display = f"{type_row['name']} ({type_row['name_ar']})" if pd.notna(type_row['name_ar']) else type_row['name']
                st.write(f"**النوع:** {type_display}")
            elif pd.notna(medication.get('drug_type_name')):
                st.write(f"**النوع:** {medication['drug_type_name']}")
        
        with col2:
            # عرض الشركة بالاسمين
            manufacturers = get_manufacturers()
            if pd.notna(medication.get('manufacturer_id')) and len(manufacturers[manufacturers['id']==medication['manufacturer_id']]) > 0:
                mfr_row = manufacturers[manufacturers['id']==medication['manufacturer_id']].iloc[0]
                mfr_display = f"{mfr_row['name']} ({mfr_row['name_ar']})" if pd.notna(mfr_row['name_ar']) else mfr_row['name']
                st.write(f"**الشركة المصنعة:** {mfr_display}")
            else:
                st.write(f"**الشركة المصنعة:** {medication['manufacturer_name']}" if pd.notna(medication.get('manufacturer_name')) else "**الشركة المصنعة:** غير محدد")
            
            st.write(f"**التركيز:** {medication['concentration']}" if pd.notna(medication.get('concentration')) else "**التركيز:** غير محدد")
            st.write(f"**الشكل الصيدلاني:** {medication['form']}" if pd.notna(medication.get('form')) else "**الشكل الصيدلاني:** غير محدد")
            st.write(f"**المادة الفعالة:** {medication['active_ingredient']}" if pd.notna(medication.get('active_ingredient')) else "**المادة الفعالة:** غير محدد")
        
        if pd.notna(medication.get('composition')):
            st.write(f"**التركيب:** {medication['composition']}")
    
    # المعلومات التجارية
    with st.expander("💰 المعلومات التجارية - Commercial Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**السعر (price):** {medication['price']} دينار" if pd.notna(medication.get('price')) else "**السعر (price):** غير محدد")
            st.write(f"**السعر مع الضريبة (price_with_tax):** {medication['price_with_tax']} دينار" if pd.notna(medication.get('price_with_tax')) else "**السعر مع الضريبة (price_with_tax):** غير محدد")
            st.write(f"**التوفر (availability):** {medication['availability']}" if pd.notna(medication.get('availability')) else "**التوفر (availability):** غير محدد")
            st.write(f"**الباركود (barcode):** {medication['barcode']}" if pd.notna(medication.get('barcode')) else "**الباركود (barcode):** غير محدد")
        
        with col2:
            st.write(f"**التعبئة (package_info):** {medication['package_info']}" if pd.notna(medication.get('package_info')) else "**التعبئة (package_info):** غير محدد")
            st.write(f"**حجم العبوة (package_size):** {medication['package_size']}" if pd.notna(medication.get('package_size')) else "**حجم العبوة (package_size):** غير محدد")
            st.write(f"**المستودع (warehouse_name):** {medication['warehouse_name']}" if pd.notna(medication.get('warehouse_name')) else "**المستودع (warehouse_name):** غير محدد")
    
    # الحدود العمرية والوزنية
    with st.expander("👶 الحدود العمرية والوزنية - Age & Weight Limits"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**الحد العمري نص (age_limit_text):** {medication['age_limit_text']}" if pd.notna(medication.get('age_limit_text')) else "**الحد العمري نص (age_limit_text):** غير محدد")
            if pd.notna(medication.get('min_age_months')) or pd.notna(medication.get('max_age_months')):
                min_age = medication.get('min_age_months', 0)
                max_age = medication.get('max_age_months', 0)
                st.write(f"**الحد العمري رقمي (min/max_age_months):** من {min_age} إلى {max_age} شهر")
        
        with col2:
            st.write(f"**الحد الوزني نص (weight_limit_text):** {medication['weight_limit_text']}" if pd.notna(medication.get('weight_limit_text')) else "**الحد الوزني نص (weight_limit_text):** غير محدد")
            if pd.notna(medication.get('min_weight_kg')) or pd.notna(medication.get('max_weight_kg')):
                min_weight = medication.get('min_weight_kg', 0)
                max_weight = medication.get('max_weight_kg', 0)
                st.write(f"**الحد الوزني رقمي (min/max_weight_kg):** من {min_weight} إلى {max_weight} كجم")
    
    # معلومات الجرعة
    with st.expander("💊 معلومات الجرعة - Dosage Information"):
        st.write(f"**الجرعة القصوى للجرعة الواحدة (max_single_dose):** {medication['max_single_dose']}" if pd.notna(medication.get('max_single_dose')) else "**الجرعة القصوى للجرعة الواحدة (max_single_dose):** غير محدد")
        st.write(f"**الجرعة القصوى اليومية (max_daily_dose):** {medication['max_daily_dose']}" if pd.notna(medication.get('max_daily_dose')) else "**الجرعة القصوى اليومية (max_daily_dose):** غير محدد")
        st.write(f"**معادلة حساب الجرعة (dose_calculation):** {medication['dose_calculation']}" if pd.notna(medication.get('dose_calculation')) else "**معادلة حساب الجرعة (dose_calculation):** غير محدد")
        st.write(f"**التكرار (frequency):** {medication['frequency']}" if pd.notna(medication.get('frequency')) else "**التكرار (frequency):** غير محدد")
        st.write(f"**المدة (duration):** {medication['duration']}" if pd.notna(medication.get('duration')) else "**المدة (duration):** غير محدد")
        st.write(f"**طريقة الإعطاء (administration_route):** {medication['administration_route']}" if pd.notna(medication.get('administration_route')) else "**طريقة الإعطاء (administration_route):** غير محدد")
    
    # المعلومات الطبية
    with st.expander("⚕️ المعلومات الطبية والصيدلانية - Medical & Pharmaceutical Information"):
        st.write(f"**دواعي الاستعمال (indications):** {medication['indications']}" if pd.notna(medication.get('indications')) else "**دواعي الاستعمال (indications):** غير محدد")
        st.write(f"**محاذير الاستخدام (contraindications):** {medication['contraindications']}" if pd.notna(medication.get('contraindications')) else "**محاذير الاستخدام (contraindications):** غير محدد")
        st.write(f"**الآثار الجانبية (side_effects):** {medication['side_effects']}" if pd.notna(medication.get('side_effects')) else "**الآثار الجانبية (side_effects):** غير محدد")
        st.write(f"**التفاعلات الدوائية (drug_interactions):** {medication['drug_interactions']}" if pd.notna(medication.get('drug_interactions')) else "**التفاعلات الدوائية (drug_interactions):** غير محدد")
        st.write(f"**تحذيرات (warnings):** {medication['warnings']}" if pd.notna(medication.get('warnings')) else "**تحذيرات (warnings):** غير محدد")
        st.write(f"**احتياطات (precautions):** {medication['precautions']}" if pd.notna(medication.get('precautions')) else "**احتياطات (precautions):** غير محدد")
        st.write(f"**إدارة الجرعة الزائدة (overdose_management):** {medication['overdose_management']}" if pd.notna(medication.get('overdose_management')) else "**إدارة الجرعة الزائدة (overdose_management):** غير محدد")
    
    # الحمل والرضاعة
    with st.expander("🤰 الحمل والرضاعة - Pregnancy & Lactation"):
        st.write(f"**فئة الحمل (pregnancy_category):** {medication['pregnancy_category']}" if pd.notna(medication.get('pregnancy_category')) else "**فئة الحمل (pregnancy_category):** غير محدد")
        st.write(f"**الأمان أثناء الحمل (pregnancy_safety):** {medication['pregnancy_safety']}" if pd.notna(medication.get('pregnancy_safety')) else "**الأمان أثناء الحمل (pregnancy_safety):** غير محدد")
        st.write(f"**الأمان أثناء الرضاعة (lactation_safety):** {medication['lactation_safety']}" if pd.notna(medication.get('lactation_safety')) else "**الأمان أثناء الرضاعة (lactation_safety):** غير محدد")
    
    # التخزين
    with st.expander("📦 التخزين - Storage Conditions"):
        st.write(f"**ظروف التخزين (storage_conditions):** {medication['storage_conditions']}" if pd.notna(medication.get('storage_conditions')) else "**ظروف التخزين (storage_conditions):** غير محدد")
        st.write(f"**مدة الصلاحية (shelf_life):** {medication['shelf_life']}" if pd.notna(medication.get('shelf_life')) else "**مدة الصلاحية (shelf_life):** غير محدد")
        st.write(f"**التخزين بعد الفتح (storage_after_opening):** {medication['storage_after_opening']}" if pd.notna(medication.get('storage_after_opening')) else "**التخزين بعد الفتح (storage_after_opening):** غير محدد")
    
    # معلومات المنشأ
    with st.expander("🌍 معلومات المنشأ - Origin Information"):
        st.write(f"**بلد التصنيع (manufacturing_country):** {medication['manufacturing_country']}" if pd.notna(medication.get('manufacturing_country')) else "**بلد التصنيع (manufacturing_country):** غير محدد")
        st.write(f"**بلد التسويق (marketing_country):** {medication['marketing_country']}" if pd.notna(medication.get('marketing_country')) else "**بلد التسويق (marketing_country):** غير محدد")
        st.write(f"**رقم الترخيص (license_number):** {medication['license_number']}" if pd.notna(medication.get('license_number')) else "**رقم الترخيص (license_number):** غير محدد")
    
    # الصور والمستندات
    with st.expander("🖼️ الصور والمستندات - Images & Documents"):
        st.write(f"**مسار صورة الدواء (image_path):** {medication['image_path']}" if pd.notna(medication.get('image_path')) else "**مسار صورة الدواء (image_path):** غير محدد")
        st.write(f"**مسار النشرة الطبية (leaflet_path):** {medication['leaflet_path']}" if pd.notna(medication.get('leaflet_path')) else "**مسار النشرة الطبية (leaflet_path):** غير محدد")
        st.write(f"**مسار صورة العلبة (box_image_path):** {medication['box_image_path']}" if pd.notna(medication.get('box_image_path')) else "**مسار صورة العلبة (box_image_path):** غير محدد")
        st.write(f"**صور إضافية (additional_images):** {medication['additional_images']}" if pd.notna(medication.get('additional_images')) else "**صور إضافية (additional_images):** غير محدد")
    
    # الملاحظات
    with st.expander("📝 ملاحظات - Notes"):
        st.write(f"**ملاحظات عامة (notes):** {medication['notes']}" if pd.notna(medication.get('notes')) else "**ملاحظات عامة (notes):** غير محدد")
        st.write(f"**ملاحظات الصيدلي (pharmacist_notes):** {medication['pharmacist_notes']}" if pd.notna(medication.get('pharmacist_notes')) else "**ملاحظات الصيدلي (pharmacist_notes):** غير محدد")
    
    # التواريخ
    with st.expander("📅 التواريخ - Timestamps"):
        st.write(f"**تاريخ الإنشاء (created_at):** {medication['created_at']}" if pd.notna(medication.get('created_at')) else "**تاريخ الإنشاء (created_at):** غير محدد")
        st.write(f"**تاريخ التحديث (updated_at):** {medication['updated_at']}" if pd.notna(medication.get('updated_at')) else "**تاريخ التحديث (updated_at):** غير محدد")

# ===================================================================
# صفحة إضافة دواء جديد
# ===================================================================
def show_add_medication_page():
    st.header("➕ إضافة دواء جديد - Add New Medication")
    
    st.info("📝 املأ الحقول المطلوبة (*) والحقول الاختيارية حسب الحاجة")
    
    with st.form("add_medication_form"):
        # ===== المعلومات الأساسية =====
        st.subheader("📌 المعلومات الأساسية - Basic Information")
        
        col1, col2 = st.columns(2)
        with col1:
            generic_name = st.text_input("الاسم العلمي * (generic_name)", placeholder="مثال: paracetamol")
            trade_name = st.text_input("الاسم التجاري (trade_name)", placeholder="مثال: Adol")
            
            categories = get_categories()
            category_id = st.selectbox(
                "الفئة (category_id)",
                options=categories['id'].tolist(),
                format_func=lambda x: f"{categories[categories['id']==x]['name'].values[0]} ({categories[categories['id']==x]['name_ar'].values[0]})" if pd.notna(categories[categories['id']==x]['name_ar'].values[0]) else categories[categories['id']==x]['name'].values[0]
            )
            
            drug_types = get_drug_types()
            if len(drug_types) > 0:
                drug_type_id = st.selectbox(
                    "نوع الدواء (drug_type_id)",
                    options=[None] + drug_types['id'].tolist(),
                    format_func=lambda x: "غير محدد" if x is None else (
                        f"{drug_types[drug_types['id']==x]['name'].values[0]} ({drug_types[drug_types['id']==x]['name_ar'].values[0]})"
                        if pd.notna(drug_types[drug_types['id']==x]['name_ar'].values[0]) 
                        else drug_types[drug_types['id']==x]['name'].values[0]
                    )
                )
            else:
                drug_type_id = None
        
        with col2:
            concentration = st.text_input("التركيز (concentration)", placeholder="مثال: 100mg/1ml")
            form = st.selectbox(
                "الشكل الصيدلاني (form)",
                ["oral drops", "suspension", "suppository", "tablet", "capsule", "syrup", "injection", "cream", "ointment", "gel", "powder"]
            )
            
            manufacturers = get_manufacturers()
            if len(manufacturers) > 0:
                manufacturer_id = st.selectbox(
                    "الشركة المصنعة (manufacturer_id)",
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
            
            active_ingredient = st.text_input("المادة الفعالة (active_ingredient)", placeholder="مثال: Paracetamol")
        
        composition = st.text_area("التركيب الكامل (composition)", placeholder="مثال: Each 1ml contains: Paracetamol 100mg", height=80)
        
        # ===== الحدود العمرية والوزنية =====
        st.markdown("---")
        st.subheader("👶 الحدود العمرية والوزنية - Age & Weight Limits")
        
        col3, col4 = st.columns(2)
        with col3:
            age_limit_text = st.text_input("الحد العمري نص (age_limit_text)", placeholder="مثال: من شهر إلى 3 سنوات")
            col3a, col3b = st.columns(2)
            with col3a:
                min_age_months = st.number_input("الحد الأدنى للعمر شهور (min_age_months)", min_value=0, value=0, step=1)
            with col3b:
                max_age_months = st.number_input("الحد الأقصى للعمر شهور (max_age_months)", min_value=0, value=0, step=1)
        
        with col4:
            weight_limit_text = st.text_input("الحد الوزني نص (weight_limit_text)", placeholder="مثال: من 4.4 إلى 14.1 كجم")
            col4a, col4b = st.columns(2)
            with col4a:
                min_weight_kg = st.number_input("الحد الأدنى للوزن كجم (min_weight_kg)", min_value=0.0, value=0.0, step=0.1)
            with col4b:
                max_weight_kg = st.number_input("الحد الأقصى للوزن كجم (max_weight_kg)", min_value=0.0, value=0.0, step=0.1)
        
        # ===== معلومات الجرعة =====
        st.markdown("---")
        st.subheader("💊 معلومات الجرعة - Dosage Information")
        
        col5, col6 = st.columns(2)
        with col5:
            max_single_dose = st.text_input("الجرعة القصوى للجرعة الواحدة (max_single_dose)", placeholder="مثال: 2 ml")
            max_daily_dose = st.text_input("الجرعة القصوى اليومية (max_daily_dose)", placeholder="مثال: 60mg/kg/day")
            frequency = st.text_input("التكرار (frequency)", placeholder="مثال: every 6 hours")
        
        with col6:
            duration = st.text_input("المدة (duration)", placeholder="مثال: 5-7 days")
            administration_route = st.selectbox(
                "طريقة الإعطاء (administration_route)",
                ["oral", "IV", "IM", "SC", "topical", "rectal", "inhalation", "other"]
            )
        
        dose_calculation = st.text_area("معادلة حساب الجرعة (dose_calculation)", placeholder="مثال: 10-15 mg/kg/dose every 6 hours", height=80)
        
        # ===== المعلومات الطبية =====
        st.markdown("---")
        st.subheader("⚕️ المعلومات الطبية والصيدلانية - Medical & Pharmaceutical Information")
        
        indications = st.text_area("دواعي الاستعمال (indications)", placeholder="مثال: خافض للحرارة ومسكن للألم", height=80)
        contraindications = st.text_area("محاذير الاستخدام (contraindications)", placeholder="مثال: فرط الحساسية للمادة الفعالة", height=80)
        side_effects = st.text_area("الآثار الجانبية (side_effects)", placeholder="مثال: غثيان، طفح جلدي", height=80)
        drug_interactions = st.text_area("التفاعلات الدوائية (drug_interactions)", placeholder="مثال: لا يستخدم مع...", height=80)
        warnings = st.text_area("تحذيرات (warnings)", placeholder="مثال: يستخدم بحذر في حالات...", height=80)
        precautions = st.text_area("احتياطات (precautions)", placeholder="مثال: يجب مراقبة...", height=80)
        overdose_management = st.text_area("إدارة الجرعة الزائدة (overdose_management)", placeholder="مثال: في حالة الجرعة الزائدة...", height=80)
        
        # ===== الحمل والرضاعة =====
        st.markdown("---")
        st.subheader("🤰 الحمل والرضاعة - Pregnancy & Lactation")
        
        col7, col8, col9 = st.columns(3)
        with col7:
            pregnancy_category = st.selectbox(
                "فئة الحمل (pregnancy_category)",
                ["", "A", "B", "C", "D", "X"]
            )
        with col8:
            pregnancy_safety = st.text_input("الأمان أثناء الحمل (pregnancy_safety)", placeholder="مثال: آمن / غير آمن")
        with col9:
            lactation_safety = st.text_input("الأمان أثناء الرضاعة (lactation_safety)", placeholder="مثال: آمن / غير آمن")
        
        # ===== ظروف التخزين =====
        st.markdown("---")
        st.subheader("📦 ظروف التخزين - Storage Conditions")
        
        col10, col11, col12 = st.columns(3)
        with col10:
            storage_conditions = st.text_input("ظروف التخزين (storage_conditions)", placeholder="مثال: يحفظ في درجة حرارة الغرفة")
        with col11:
            shelf_life = st.text_input("مدة الصلاحية (shelf_life)", placeholder="مثال: 3 سنوات")
        with col12:
            storage_after_opening = st.text_input("التخزين بعد الفتح (storage_after_opening)", placeholder="مثال: يستخدم خلال شهر")
        
        # ===== المعلومات التجارية =====
        st.markdown("---")
        st.subheader("💰 المعلومات التجارية - Commercial Information")
        
        col13, col14 = st.columns(2)
        with col13:
            price = st.number_input("السعر دينار (price)", min_value=0.0, step=0.1)
            price_with_tax = st.number_input("السعر مع الضريبة دينار (price_with_tax)", min_value=0.0, step=0.1)
            availability = st.selectbox("التوفر (availability)", ["متوفر", "غير متوفر", "نادر"])
        
        with col14:
            package_info = st.text_input("التعبئة (package_info)", placeholder="مثال: 15ml bottle")
            package_size = st.text_input("حجم العبوة (package_size)", placeholder="مثال: 15ml")
            barcode = st.text_input("الباركود (barcode)", placeholder="مثال: 1234567890123")
        
        warehouse_name = st.text_input("اسم المستودع (warehouse_name)", placeholder="مثال: المستودع الرئيسي")
        
        # ===== معلومات المنشأ =====
        st.markdown("---")
        st.subheader("🌍 معلومات المنشأ - Origin Information")
        
        col15, col16, col17 = st.columns(3)
        with col15:
            manufacturing_country = st.text_input("بلد التصنيع (manufacturing_country)", placeholder="مثال: Jordan")
        with col16:
            marketing_country = st.text_input("بلد التسويق (marketing_country)", placeholder="مثال: Jordan")
        with col17:
            license_number = st.text_input("رقم الترخيص (license_number)", placeholder="مثال: 12345/2023")
        
        # ===== الصور والمستندات =====
        st.markdown("---")
        st.subheader("🖼️ الصور والمستندات - Images & Documents")
        
        col18, col19 = st.columns(2)
        with col18:
            image_path = st.text_input("مسار صورة الدواء (image_path)", placeholder="مثال: images/drug1.jpg")
            leaflet_path = st.text_input("مسار النشرة الطبية (leaflet_path)", placeholder="مثال: leaflets/drug1.pdf")
        with col19:
            box_image_path = st.text_input("مسار صورة العلبة (box_image_path)", placeholder="مثال: images/box1.jpg")
            additional_images = st.text_area("صور إضافية (additional_images)", placeholder="مثال: img1.jpg, img2.jpg", height=60)
        
        # ===== ملاحظات =====
        st.markdown("---")
        st.subheader("📝 ملاحظات - Notes")
        
        notes = st.text_area("ملاحظات عامة (notes)", placeholder="أي ملاحظات إضافية", height=80)
        pharmacist_notes = st.text_area("ملاحظات الصيدلي (pharmacist_notes)", placeholder="ملاحظات خاصة بالصيدلي", height=80)
        
        # ===== زر الحفظ =====
        st.markdown("---")
        submitted = st.form_submit_button("💾 حفظ الدواء", use_container_width=True, type="primary")
        
        if submitted:
            if not generic_name:
                st.error("❌ الرجاء إدخال الاسم العلمي على الأقل")
            else:
                medication_data = {
                    'generic_name': generic_name,
                    'trade_name': trade_name if trade_name else None,
                    'category_id': category_id,
                    'drug_type_id': drug_type_id,
                    'manufacturer_id': manufacturer_id,
                    'concentration': concentration if concentration else None,
                    'form': form,
                    'active_ingredient': active_ingredient if active_ingredient else None,
                    'composition': composition if composition else None,
                    'min_age_months': min_age_months if min_age_months > 0 else None,
                    'max_age_months': max_age_months if max_age_months > 0 else None,
                    'age_limit_text': age_limit_text if age_limit_text else None,
                    'min_weight_kg': min_weight_kg if min_weight_kg > 0 else None,
                    'max_weight_kg': max_weight_kg if max_weight_kg > 0 else None,
                    'weight_limit_text': weight_limit_text if weight_limit_text else None,
                    'max_single_dose': max_single_dose if max_single_dose else None,
                    'dose_calculation': dose_calculation if dose_calculation else None,
                    'max_daily_dose': max_daily_dose if max_daily_dose else None,
                    'frequency': frequency if frequency else None,
                    'duration': duration if duration else None,
                    'administration_route': administration_route if administration_route else None,
                    'indications': indications if indications else None,
                    'contraindications': contraindications if contraindications else None,
                    'side_effects': side_effects if side_effects else None,
                    'drug_interactions': drug_interactions if drug_interactions else None,
                    'warnings': warnings if warnings else None,
                    'precautions': precautions if precautions else None,
                    'overdose_management': overdose_management if overdose_management else None,
                    'pregnancy_category': pregnancy_category if pregnancy_category else None,
                    'pregnancy_safety': pregnancy_safety if pregnancy_safety else None,
                    'lactation_safety': lactation_safety if lactation_safety else None,
                    'storage_conditions': storage_conditions if storage_conditions else None,
                    'shelf_life': shelf_life if shelf_life else None,
                    'storage_after_opening': storage_after_opening if storage_after_opening else None,
                    'warehouse_name': warehouse_name if warehouse_name else None,
                    'package_info': package_info if package_info else None,
                    'package_size': package_size if package_size else None,
                    'price': price if price > 0 else None,
                    'price_with_tax': price_with_tax if price_with_tax > 0 else None,
                    'availability': availability,
                    'barcode': barcode if barcode else None,
                    'image_path': image_path if image_path else None,
                    'leaflet_path': leaflet_path if leaflet_path else None,
                    'box_image_path': box_image_path if box_image_path else None,
                    'additional_images': additional_images if additional_images else None,
                    'manufacturing_country': manufacturing_country if manufacturing_country else None,
                    'marketing_country': marketing_country if marketing_country else None,
                    'license_number': license_number if license_number else None,
                    'notes': notes if notes else None,
                    'pharmacist_notes': pharmacist_notes if pharmacist_notes else None,
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
    
    if len(manufacturers) > 0:
        # عرض مع خيارات الحذف
        for idx, row in manufacturers.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
            with col1:
                st.write(f"**{row['id']}**")
            with col2:
                st.write(row['name'])
            with col3:
                st.write(row['name_ar'] if pd.notna(row['name_ar']) else "-")
            with col4:
                st.write(row['country'] if pd.notna(row['country']) else "-")
            with col5:
                if st.button("🗑️", key=f"del_mfr_{row['id']}"):
                    try:
                        delete_manufacturer(row['id'])
                        st.success(f"✅ تم حذف الشركة")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
    else:
        st.info("لا توجد شركات مصنعة")
    
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
# صفحة عرض قاعدة البيانات الكاملة
# ===================================================================
def show_database_viewer_page():
    st.header("🗄️ عرض قاعدة البيانات الكاملة")
    
    st.info("📊 هذه الصفحة تعرض جميع البيانات في قاعدة البيانات مع إمكانية الحذف")
    
    # شرح هيكل قاعدة البيانات
    with st.expander("📚 فهم هيكل قاعدة البيانات - Understanding Database Structure"):
        st.markdown("""
        ### الجداول الرئيسية في قاعدة البيانات:
        
        1. **medications (الأدوية)** 💊
           - الجدول الرئيسي الذي يحتوي على جميع معلومات الأدوية
           - يحتوي على: الاسم العلمي، الاسم التجاري، التركيز، الجرعات، الأسعار، إلخ
        
        2. **categories (الفئات)** 📂
           - تصنيفات الأدوية حسب الفئة المستهدفة
           - أمثلة: أطفال (pediatric)، بالغين (adult)، حوامل (pregnant)
        
        3. **drug_types (أنواع الأدوية)** 🔢
           - تصنيفات الأدوية حسب النوع الدوائي
           - أمثلة: مضاد حيوي (antibiotic)، خافض حرارة (antipyretics)
        
        4. **manufacturers (الشركات المصنعة)** 🏭
           - معلومات الشركات المصنعة للأدوية
           - يحتوي على: اسم الشركة، البلد، الموقع الإلكتروني
        
        5. **age_weight_estimates (تقديرات الأوزان)** 📊
           - جدول مرجعي لتقدير وزن الطفل حسب العمر
           - يستخدم لحساب الجرعات المناسبة
        
        ---
        
        ### العلاقات بين الجداول:
        - كل دواء (medication) مرتبط بـ:
          - فئة واحدة (category)
          - نوع دواء واحد (drug_type)
          - شركة مصنعة واحدة (manufacturer)
        """)
    
    # إحصائيات سريعة
    meds_df = get_all_medications()
    cats_df = get_categories()
    types_df = get_drug_types()
    manufacturers_df = get_manufacturers()
    weights_df = get_age_weight_estimates()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💊 الأدوية", len(meds_df))
    with col2:
        st.metric("📂 الفئات", len(cats_df))
    with col3:
        st.metric("🔢 الأنواع", len(types_df))
    with col4:
        st.metric("🏭 الشركات", len(manufacturers_df))
    with col5:
        st.metric("📊 الأوزان", len(weights_df))
    
    st.markdown("---")
    
    # عرض الجداول في تبويبات
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💊 الأدوية (Medications)", 
        "📂 الفئات (Categories)", 
        "🔢 أنواع الأدوية (Drug Types)", 
        "🏭 الشركات المصنعة (Manufacturers)",
        "📊 تقديرات الأوزان (Age Weight Estimates)"
    ])
    
    # تبويب الأدوية
    with tab1:
        st.subheader("💊 جميع الأدوية (Medications Table)")
        st.caption("📋 الجدول: medications | يحتوي على معلومات الأدوية الكاملة")
        if len(meds_df) > 0:
            st.dataframe(meds_df, use_container_width=True, height=400)
            
            st.markdown("---")
            st.subheader("🗑️ حذف دواء")
            
            col_select, col_delete = st.columns([3, 1])
            with col_select:
                med_to_delete = st.selectbox(
                    "اختر دواء للحذف",
                    meds_df['id'].tolist(),
                    format_func=lambda x: f"ID:{x} - {meds_df[meds_df['id']==x]['generic_name'].values[0]} ({meds_df[meds_df['id']==x]['trade_name'].values[0]})",
                    key="delete_med_select"
                )
            
            with col_delete:
                st.write("")
                st.write("")
                if st.button("🗑️ حذف", key="delete_med_btn", type="secondary"):
                    try:
                        delete_medication(med_to_delete)
                        st.success(f"✅ تم حذف الدواء ID:{med_to_delete}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
        else:
            st.info("لا توجد أدوية في قاعدة البيانات")
    
    # تبويب الفئات
    with tab2:
        st.subheader("📂 جميع الفئات (Categories Table)")
        st.caption("📋 الجدول: categories | يحتوي على تصنيفات الأدوية (أطفال، بالغين، حوامل، إلخ)")
        if len(cats_df) > 0:
            # عرض الجدول
            st.dataframe(cats_df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🗑️ حذف فئة")
            
            for idx, row in cats_df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 1])
                with col1:
                    st.write(f"**{row['id']}**")
                with col2:
                    st.write(row['name'])
                with col3:
                    st.write(row['name_ar'] if pd.notna(row['name_ar']) else "-")
                with col4:
                    st.write(row['description'][:50] + "..." if pd.notna(row['description']) and len(str(row['description'])) > 50 else (row['description'] if pd.notna(row['description']) else "-"))
                with col5:
                    if st.button("🗑️", key=f"db_del_cat_{row['id']}"):
                        try:
                            delete_category(row['id'])
                            st.success(f"✅ تم حذف الفئة")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ: {str(e)}")
        else:
            st.info("لا توجد فئات في قاعدة البيانات")
    
    # تبويب أنواع الأدوية
    with tab3:
        st.subheader("🔢 جميع أنواع الأدوية (Drug Types Table)")
        st.caption("📋 الجدول: drug_types | يحتوي على أنواع الأدوية (مضاد حيوي، خافض حرارة، إلخ)")
        if len(types_df) > 0:
            # عرض الجدول
            st.dataframe(types_df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🗑️ حذف نوع دواء")
            
            for idx, row in types_df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 1])
                with col1:
                    st.write(f"**{row['id']}**")
                with col2:
                    st.write(row['name'])
                with col3:
                    st.write(row['name_ar'] if pd.notna(row['name_ar']) else "-")
                with col4:
                    st.write(row['description'][:50] + "..." if pd.notna(row['description']) and len(str(row['description'])) > 50 else (row['description'] if pd.notna(row['description']) else "-"))
                with col5:
                    if st.button("🗑️", key=f"db_del_type_{row['id']}"):
                        try:
                            delete_drug_type(row['id'])
                            st.success(f"✅ تم حذف النوع")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ: {str(e)}")
        else:
            st.info("لا توجد أنواع أدوية في قاعدة البيانات")
    
    # تبويب الشركات المصنعة
    with tab4:
        st.subheader("🏭 جميع الشركات المصنعة (Manufacturers Table)")
        st.caption("📋 الجدول: manufacturers | يحتوي على معلومات الشركات المصنعة للأدوية")
        if len(manufacturers_df) > 0:
            # عرض الجدول
            st.dataframe(manufacturers_df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🗑️ حذف شركة مصنعة")
            
            for idx, row in manufacturers_df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
                with col1:
                    st.write(f"**{row['id']}**")
                with col2:
                    st.write(row['name'])
                with col3:
                    st.write(row['name_ar'] if pd.notna(row['name_ar']) else "-")
                with col4:
                    st.write(row['country'] if pd.notna(row['country']) else "-")
                with col5:
                    if st.button("🗑️", key=f"db_del_mfr_{row['id']}"):
                        try:
                            delete_manufacturer(row['id'])
                            st.success(f"✅ تم حذف الشركة")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ: {str(e)}")
        else:
            st.info("لا توجد شركات مصنعة في قاعدة البيانات")
    
    # تبويب تقديرات الأوزان
    with tab5:
        st.subheader("📊 تقديرات الأوزان حسب العمر (Age Weight Estimates Table)")
        st.caption("📋 الجدول: age_weight_estimates | يحتوي على تقديرات الأوزان المتوقعة حسب عمر الطفل")
        if len(weights_df) > 0:
            st.dataframe(weights_df, use_container_width=True, height=400)
            st.info("ℹ️ هذا الجدول للقراءة فقط - لا يمكن حذف البيانات")
        else:
            st.info("لا توجد بيانات تقديرات الأوزان")
    
    st.markdown("---")
    
    # خيارات متقدمة
    with st.expander("⚙️ خيارات متقدمة"):
        st.warning("⚠️ تحذير: هذه العمليات لا يمكن التراجع عنها!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ حذف جميع الأدوية", type="secondary"):
                if st.session_state.get('confirm_delete_all_meds', False):
                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM medications")
                        conn.commit()
                        conn.close()
                        st.success("✅ تم حذف جميع الأدوية")
                        st.session_state['confirm_delete_all_meds'] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
                else:
                    st.session_state['confirm_delete_all_meds'] = True
                    st.warning("⚠️ انقر مرة أخرى للتأكيد")
        
        with col2:
            if st.button("📊 عرض معلومات قاعدة البيانات", type="primary"):
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # الحصول على حجم قاعدة البيانات
                db_size = os.path.getsize(DB_PATH) / 1024  # KB
                st.metric("حجم قاعدة البيانات", f"{db_size:.2f} KB")
                
                # الحصول على قائمة الجداول مع الترجمة العربية
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                # قاموس الترجمة للجداول
                table_translations = {
                    'medications': 'الأدوية',
                    'categories': 'الفئات',
                    'drug_types': 'أنواع الأدوية',
                    'manufacturers': 'الشركات المصنعة',
                    'age_weight_estimates': 'تقديرات الأوزان حسب العمر',
                    'search_history': 'سجل البحث'
                }
                
                st.write("**الجداول المتوفرة في قاعدة البيانات:**")
                for table in tables:
                    table_name = table[0]
                    arabic_name = table_translations.get(table_name, table_name)
                    
                    # عد السجلات في كل جدول
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        st.write(f"- **{table_name}** ({arabic_name}) - {count} سجل")
                    except:
                        st.write(f"- **{table_name}** ({arabic_name})")
                
                conn.close()

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
