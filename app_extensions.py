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
                    st.success(f" تم إضافة نوع {name} بنجاح!")
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
