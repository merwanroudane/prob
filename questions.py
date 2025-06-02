import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import networkx as nx

# تعيين إعدادات الصفحة
st.set_page_config(
	page_title="مخطط معالجة الإشكاليات في الدراسات القياسية",
	page_icon="📊",
	layout="wide",
	initial_sidebar_state="expanded",
)

# تعريف CSS للاتجاه من اليمين إلى اليسار
st.markdown("""
<style>
    .rtl {
        direction: rtl;
        text-align: right;
    }
    .sidebar .sidebar-content {
        direction: rtl;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        direction: rtl;
        text-align: right;
    }
    .stButton button {
        font-family: 'Arial', sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1E3D59;
        text-align: center;
        padding: 20px 0;
        background-color: #F5F5F5;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 28px;
        font-weight: bold;
        color: #2B6777;
        border-bottom: 2px solid #2B6777;
        padding-bottom: 10px;
        margin: 30px 0 20px 0;
    }
    .section-header {
        font-size: 22px;
        font-weight: bold;
        color: #006D77;
        margin: 20px 0 10px 0;
    }
    .note-box {
        background-color: #FFDDD2;
        border-left: 5px solid #E29578;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    .model-box {
        background-color: #E8F1F2;
        border-left: 5px solid #006D77;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .highlight {
        color: #006D77;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="main-header rtl">مخطط معالجة الإشكاليات في الدراسات القياسية</div>', unsafe_allow_html=True)

# إنشاء القائمة الجانبية
st.sidebar.markdown('<h2 class="rtl">الإشكاليات القياسية</h2>', unsafe_allow_html=True)

# إضافة خيارات التنقل في القائمة الجانبية
page = st.sidebar.radio(
	"اختر الإشكالية للعرض:",
	[
		"نظرة عامة",
		"إشكالية الأثر والتأثير",
		"إشكالية المقارنة",
		"إشكالية المحددات",
		"إشكالية السببية",
		"إشكالية الفعالية",
		"إشكالية التنبؤ",
		"إشكالية الأجل الطويل والأجل القصير",
		"الإشكالية المدمجة"
	]
)

# إضافة ملاحظات إلى القائمة الجانبية
st.sidebar.markdown('<div class="note-box rtl">', unsafe_allow_html=True)
st.sidebar.markdown("""
<h3>ملاحظات:</h3>
<ul>
    <li>هذا المخطط خاص بالإشكاليات العامة وليست الإشكاليات المتخصصة مثل نماذج تسعير الخيارات المالية.</li>
    <li>هذا المخطط لا يعني أنه شامل لكل الحالات، قد تكون هناك حالات أخرى.</li>
    <li>يجب الانتباه للكلمات المفتاحية في العناوين لأنها تلعب دور كبير في توجيه الباحث للمناهج المناسبة.</li>
    <li>مهما كانت طبيعة النموذج إلا أنه دوما يبقى محدود ولهذا على الباحث أن يحسن من نموذجه.</li>
</ul>
""", unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)


# دالة لإنشاء مخطط شبكي للإشكاليات
def create_network_chart():
	G = nx.DiGraph()

	# إضافة العقد (الإشكاليات)
	issues = [
		"إشكالية الأثر والتأثير", "إشكالية المقارنة", "إشكالية المحددات",
		"إشكالية السببية", "إشكالية الفعالية", "إشكالية التنبؤ",
		"إشكالية الأجل الطويل والأجل القصير", "الإشكالية المدمجة"
	]

	# إضافة العقد مع ألوان مختلفة
	node_colors = ["#FF9671", "#FFC75F", "#F9F871", "#D65DB1", "#845EC2", "#00C9A7", "#4D8076", "#4E8397"]
	for i, issue in enumerate(issues):
		G.add_node(issue, color=node_colors[i])

	# إضافة الروابط
	G.add_edge("إشكالية الأثر والتأثير", "إشكالية السببية")
	G.add_edge("إشكالية السببية", "إشكالية الفعالية")
	G.add_edge("إشكالية الأثر والتأثير", "إشكالية المقارنة")
	G.add_edge("إشكالية المقارنة", "إشكالية المحددات")
	G.add_edge("إشكالية التنبؤ", "إشكالية الأجل الطويل والأجل القصير")
	G.add_edge("إشكالية الأجل الطويل والأجل القصير", "الإشكالية المدمجة")
	G.add_edge("إشكالية السببية", "الإشكالية المدمجة")
	G.add_edge("إشكالية المحددات", "الإشكالية المدمجة")

	# استخدام خوارزمية تخطيط spring_layout لتحديد مواقع العقد
	pos = nx.spring_layout(G, seed=42)

	# إنشاء قوائم للرسم
	edge_x = []
	edge_y = []
	for edge in G.edges():
		x0, y0 = pos[edge[0]]
		x1, y1 = pos[edge[1]]
		edge_x.extend([x0, x1, None])
		edge_y.extend([y0, y1, None])

	edge_trace = go.Scatter(
		x=edge_x, y=edge_y,
		line=dict(width=2, color='#888'),
		hoverinfo='none',
		mode='lines')

	node_x = []
	node_y = []
	node_colors = []
	node_text = []

	for node in G.nodes():
		x, y = pos[node]
		node_x.append(x)
		node_y.append(y)
		node_colors.append(G.nodes[node]['color'])
		node_text.append(node)

	node_trace = go.Scatter(
		x=node_x, y=node_y,
		mode='markers+text',
		hoverinfo='text',
		text=node_text,
		textposition="top center",
		marker=dict(
			showscale=False,
			color=node_colors,
			size=30,
			line_width=2))

	fig = go.Figure(data=[edge_trace, node_trace],
					layout=go.Layout(
						title="<b>العلاقات بين الإشكاليات في الدراسات القياسية</b>",
						titlefont_size=16,
						showlegend=False,
						hovermode='closest',
						margin=dict(b=20, l=5, r=5, t=40),
						xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
						yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
						height=600,
						plot_bgcolor='rgba(0,0,0,0)'
					))

	fig.update_layout(
		font=dict(
			family="Arial",
			size=14,
		)
	)

	return fig


# دالة لإنشاء مخطط هيكلي للنماذج
def create_model_hierarchy(category, models):
	fig = go.Figure(go.Treemap(
		labels=models,
		parents=[""] + [category] * (len(models) - 1),
		text=models,
		textinfo="label",
		hoverinfo="label+text",
		marker=dict(
			colorscale='Viridis',
			cmid=0.5
		),
	))

	fig.update_layout(
		title=f"<b>أنواع النماذج في {category}</b>",
		font=dict(
			size=14,
			family="Arial"
		),
		margin=dict(t=50, l=25, r=25, b=25),
		height=400,
	)

	return fig


# دالة لإنشاء مخطط عملية حل الإشكاليات
def create_process_flow(steps):
	# إنشاء الأسهم
	annotations = []
	for i in range(len(steps) - 1):
		annotations.append(dict(
			x=0.5,
			y=0.9 - i * 0.2,
			xref="paper",
			yref="paper",
			text="↓",
			showarrow=False,
			font=dict(size=24),
		))

	# إنشاء المخطط
	fig = go.Figure()

	for i, step in enumerate(steps):
		fig.add_trace(go.Scatter(
			x=[0.5],
			y=[0.9 - i * 0.2 - 0.1],
			mode="markers+text",
			marker=dict(size=30, color=px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]),
			text=[step],
			textposition="middle center",
			textfont=dict(size=14),
			name=step
		))

	fig.update_layout(
		title="<b>خطوات معالجة الإشكالية</b>",
		showlegend=False,
		annotations=annotations,
		xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
		yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
		height=100 + 100 * len(steps),
		margin=dict(l=10, r=10, t=50, b=10),
		plot_bgcolor='rgba(0,0,0,0)'
	)

	return fig


# دالة لإنشاء رسم بياني شريطي لمقارنة النماذج
def create_model_comparison_chart(models, aspects):
	z_values = np.random.randint(1, 10, size=(len(models), len(aspects)))

	fig = go.Figure(data=go.Heatmap(
		z=z_values,
		x=aspects,
		y=models,
		colorscale='Viridis',
		colorbar=dict(title="الأداء"),
	))

	fig.update_layout(
		title="<b>مقارنة بين النماذج وفق جوانب مختلفة</b>",
		xaxis_title="الجوانب",
		yaxis_title="النماذج",
		height=400,
		font=dict(
			family="Arial",
			size=14
		)
	)

	return fig


# عرض المحتوى بناءً على الصفحة المختارة
if page == "نظرة عامة":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">نظرة عامة على الإشكاليات في الدراسات القياسية</h2>

    <p>
    تواجه الدراسات القياسية في مجال الاقتصاد والمالية والعلوم الاجتماعية العديد من الإشكاليات المنهجية والتحليلية التي تؤثر على دقة النتائج وموثوقيتها. يقدم هذا المخطط تصنيفاً منهجياً للإشكاليات الرئيسية ويستعرض النماذج والأساليب المناسبة لمعالجة كل إشكالية.
    </p>

    <p>
    تتضمن الإشكاليات الرئيسية في الدراسات القياسية:
    </p>

    <ol>
        <li><span class="highlight">إشكالية الأثر والتأثير</span>: تتعلق بتحديد وقياس الآثار المباشرة وغير المباشرة للمتغيرات.</li>
        <li><span class="highlight">إشكالية المقارنة</span>: تتعلق بالمقارنة بين النماذج أو المعلمات أو النتائج.</li>
        <li><span class="highlight">إشكالية المحددات</span>: تتعلق بتحديد العوامل الأكثر تأثيراً في الظاهرة المدروسة.</li>
        <li><span class="highlight">إشكالية السببية</span>: تتعلق بتحديد العلاقات السببية بين المتغيرات.</li>
        <li><span class="highlight">إشكالية الفعالية</span>: تتعلق بقياس فعالية السياسات أو التدخلات.</li>
        <li><span class="highlight">إشكالية التنبؤ</span>: تتعلق بالقدرة على التنبؤ بالمستقبل انطلاقاً من البيانات المتاحة.</li>
        <li><span class="highlight">إشكالية الأجل الطويل والأجل القصير</span>: تتعلق بتحليل العلاقات في الآجال المختلفة.</li>
        <li><span class="highlight">الإشكالية المدمجة</span>: تتعلق بالجمع بين عدة إشكاليات أو نماذج.</li>
    </ol>

    <p>
    يجب على الباحث اختيار النماذج والأساليب المناسبة بناءً على طبيعة الإشكالية المطروحة، مع الأخذ بعين الاعتبار خصائص البيانات المتاحة والهدف من الدراسة.
    </p>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط العلاقات بين الإشكاليات
	st.plotly_chart(create_network_chart(), use_container_width=True)

	# أمثلة للمنهجيات الشائعة
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">أمثلة للمنهجيات الشائعة في الدراسات القياسية</h3>
    <div class="model-box">
    <ul>
        <li>نموذج الانحدار بالفروق، ECM، VECM، VAR، منهجية ARDL Bound test، SVAR، SVECM، إلخ...</li>
        <li>نماذج الاستدلال السببي: Causal impact model، Causal var، Causal arima، Causal inference</li>
        <li>خوارزميات التعلم الآلي: طرق اختيار المتغيرات، الغابة العشوائية، الشبكات العصبية العميقة</li>
        <li>النماذج الديناميكية: نماذج التأثير الديناميكي، نماذج التأثير الديناميكي الموزع، نماذج ذات المعاملات المتغيرة</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

elif page == "إشكالية الأثر والتأثير":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية الأثر والتأثير</h2>

    <p>
    تُعنى إشكالية الأثر والتأثير بدراسة وقياس العلاقات بين المتغيرات وتحديد حجم وطبيعة التأثيرات بينها. تتعدد أنواع التأثيرات في الدراسات القياسية، مما يتطلب اختيار النماذج المناسبة لكل نوع.
    </p>

    <h3 class="section-header">أنواع التأثير:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# إنشاء مخطط لأنواع التأثير
	impact_types = [
		"التأثير",
		"التأثير الساكن", "التأثير الديناميكي", "التأثير غير المباشر", "التأثير الغير متعلق بالمتوسط"
	]
	dynamic_types = [
		"التأثير الديناميكي",
		"التأثير الديناميكي الموزع", "التأثير الديناميكي الكلي",
		"التأثير الديناميكي ذو المعاملات المتغيرة", "التأثير الديناميكي المبني على التوقعات"
	]

	# عرض مخطط أنواع التأثير
	st.plotly_chart(create_model_hierarchy("التأثير", impact_types), use_container_width=True)

	# عرض مخطط أنواع التأثير الديناميكي
	st.plotly_chart(create_model_hierarchy("التأثير الديناميكي", dynamic_types), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">النماذج المستخدمة في تحليل الأثر والتأثير:</h3>

    <h4>1. نماذج التأثير الساكن:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات الثابتة عبر الزمن، ومن أمثلتها:
    </p>
    <ul>
        <li>الانحدار الخطي البسيط والمتعدد</li>
        <li>نماذج متعددة المعادلات</li>
        <li>نماذج البيانات المقطعية Cross-sectional data</li>
    </ul>
    </div>

    <h4>2. نماذج التأثير الديناميكي:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات المتغيرة عبر الزمن، ومن أمثلتها:
    </p>
    <ul>
        <li>نماذج الانحدار بالفروق (Differenced Regression)</li>
        <li>نماذج تصحيح الخطأ (ECM)</li>
        <li>نماذج متجه تصحيح الخطأ (VECM)</li>
        <li>نماذج الانحدار الذاتي ذو الفجوات الموزعة (ARDL)</li>
        <li>نماذج متجه الانحدار الذاتي (VAR)</li>
    </ul>
    </div>

    <h4>3. نماذج التأثير الديناميكي الموزع:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات الموزعة عبر فترات زمنية متعددة، ومن أمثلتها:
    </p>
    <ul>
        <li>نموذج الفجوات الموزعة (DL)</li>
        <li>نموذج الانحدار الذاتي ذو الفجوات الموزعة (ARDL)</li>
        <li>نموذج الفجوات الموزعة المتعددة (PDL)</li>
        <li>نموذج الفجوات الموزعة العامة (GDL)</li>
    </ul>
    </div>

    <h4>4. نماذج التأثير الديناميكي ذو المعاملات المتغيرة:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات التي تتغير معاملاتها عبر الزمن، ومن أمثلتها:
    </p>
    <ul>
        <li>عائلة نماذج المعاملات المتغيرة زمنياً (Time-varying parameters)</li>
        <li>نماذج التحول الهيكلي (Structural break models)</li>
        <li>نماذج التبديل الماركوفي (Markov switching models)</li>
    </ul>
    </div>

    <h4>5. نماذج التأثير الديناميكي المبني على التوقعات:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات المبنية على توقعات الأفراد والمؤسسات، ومن أمثلتها:
    </p>
    <ul>
        <li>نماذج التوقعات المكيفة والرشيدة</li>
        <li>نماذج التوقعات الرشيدة المحدودة</li>
        <li>نماذج التعلم التكيفي (Adaptive learning)</li>
    </ul>
    </div>

    <h4>6. نماذج التأثير غير المباشر:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات التي تتم عبر متغيرات وسيطة، ومن أمثلتها:
    </p>
    <ul>
        <li>نماذج تحليل المسار الساكن والديناميكي</li>
        <li>نماذج المعادلات البنائية (SEM)</li>
        <li>نماذج الوساطة (Mediation models)</li>
    </ul>
    </div>

    <h4>7. نماذج التأثير الغير متعلق بالمتوسط:</h4>
    <div class="model-box">
    <p>
    تستخدم لقياس التأثيرات على جوانب أخرى من التوزيع غير المتوسط، ومن أمثلتها:
    </p>
    <ul>
        <li>انحدار الكميات (Quantile regression)</li>
        <li>انحدار الكميات ذو الفجوات الموزعة (Quantile ARDL)</li>
        <li>كميات في كميات (Quantile in quantile)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط عملية اختيار النموذج المناسب
	steps = [
		"تحديد نوع التأثير المراد دراسته",
		"فحص خصائص البيانات",
		"اختبار استقرارية السلاسل الزمنية",
		"تحديد النموذج المناسب",
		"تقدير النموذج وفحص الجودة",
		"تفسير النتائج وتحليلها"
	]
	st.plotly_chart(create_process_flow(steps), use_container_width=True)

elif page == "إشكالية المقارنة":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية المقارنة</h2>

    <p>
    تتعلق إشكالية المقارنة بالمقارنة بين النماذج أو المعلمات أو النتائج أو بين مجموعات مختلفة (دول، قطاعات، مؤسسات، إلخ). تتطلب هذه الإشكالية اختيار منهجيات مناسبة تضمن المقارنة العادلة والموضوعية.
    </p>

    <h3 class="section-header">أنواع المقارنات:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# إنشاء مخطط لأنواع المقارنة
	comparison_types = [
		"المقارنة",
		"المقارنة بالنماذج", "المقارنة الوصفية"
	]

	# عرض مخطط أنواع المقارنة
	st.plotly_chart(create_model_hierarchy("المقارنة", comparison_types), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">منهجيات المقارنة:</h3>

    <h4>1. المقارنة بالنماذج:</h4>
    <div class="model-box">
    <p>
    تتضمن المقارنة بين نماذج مختلفة أو مجموعات مختلفة باستخدام النماذج القياسية، ومن أمثلتها:
    </p>
    <ul>
        <li>المقارنة بالمعلمات تحت شروط معينة</li>
        <li>المقارنة بالخصائص الاحتمالية للنماذج</li>
        <li>المقارنة بالأهداف النهائية</li>
        <li>نماذج البانل مع استخراج الآثار الفردية</li>
        <li>نماذج القطاعات (Sectoral models)</li>
        <li>نماذج السلاسل الزمنية المتشابكة</li>
        <li>نماذج الدول المتقاطعة (Cross-country analysis)</li>
        <li>نماذج الشبكات (Network Model)</li>
        <li>بيانات البانل الشبكية (Network Panel Data)</li>
        <li>نماذج متجه الانحدار الذاتي العالمية (GVAR)</li>
        <li>تحليل قبل وبعد (Before After Analysis)</li>
    </ul>
    </div>

    <h4>2. المقارنة الوصفية:</h4>
    <div class="model-box">
    <p>
    تعتمد على الإحصاء الوصفي والتحليل البصري للبيانات، ومن أمثلتها:
    </p>
    <ul>
        <li>مقارنة باستخدام مؤشرات الإحصاء الوصفي مثل معامل الاختلاف</li>
        <li>مقارنة بالمقاربات الاحتمالية</li>
        <li>استخدام أدوات تصور البيانات (Data Visualization)</li>
        <li>مخططات الصناديق (Box plots)</li>
        <li>مخططات الانتشار (Scatter plots)</li>
        <li>خرائط الحرارة (Heat maps)</li>
    </ul>
    </div>

    <h3 class="section-header">أهم الاختبارات الإحصائية المستخدمة في المقارنة:</h3>
    <div class="model-box">
    <ul>
        <li>اختبار t للمقارنة بين متوسطين</li>
        <li>تحليل التباين (ANOVA) للمقارنة بين عدة مجموعات</li>
        <li>اختبار Hausman للمقارنة بين نماذج البانل</li>
        <li>اختبار نسبة الأرجحية (Likelihood Ratio Test)</li>
        <li>معايير المعلومات (AIC, BIC, HQ) للمقارنة بين النماذج</li>
        <li>اختبار Diebold-Mariano للمقارنة بين دقة التنبؤات</li>
        <li>اختبار J لمقارنة النماذج المتداخلة</li>
        <li>اختبار Davidson-MacKinnon للمقارنة بين النماذج غير المتداخلة</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# إنشاء مخطط مقارنة النماذج
	models = ["نموذج انحدار خطي", "نموذج VAR", "نموذج ARDL", "نموذج ECM", "نموذج GARCH"]
	aspects = ["دقة التنبؤ", "القدرة التفسيرية", "سهولة التفسير", "تعقيد النموذج", "المرونة"]

	st.plotly_chart(create_model_comparison_chart(models, aspects), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">خطوات إجراء المقارنة:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط خطوات المقارنة
	comparison_steps = [
		"تحديد الهدف من المقارنة",
		"اختيار المجموعات أو النماذج للمقارنة",
		"تحديد معايير المقارنة",
		"اختيار المنهجية المناسبة",
		"جمع وتحليل البيانات",
		"إجراء الاختبارات الإحصائية المناسبة",
		"تفسير النتائج واستخلاص الاستنتاجات"
	]

	st.plotly_chart(create_process_flow(comparison_steps), use_container_width=True)

elif page == "إشكالية المحددات":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية المحددات</h2>

    <p>
    تتعلق إشكالية المحددات بتحديد العوامل الأكثر تأثيراً في الظاهرة المدروسة واختيار المتغيرات المناسبة للنموذج. تعتبر هذه الإشكالية أساسية في بناء النماذج القياسية الفعالة والتي تتسم بالقدرة التفسيرية العالية.
    </p>

    <h3 class="section-header">طرق تحديد واختيار المتغيرات:</h3>
    <div class="model-box">
    <ul>
        <li>نموذج الانحدار المعياري (Standard Regression)</li>
        <li>طرق الأهمية النسبية (Relative Importance)</li>
        <li>خوارزميات اختيار المتغيرات (Variable Selection Methods):
            <ul>
                <li>الاختيار التدريجي (Stepwise Selection)</li>
                <li>الاختيار الأمامي (Forward Selection)</li>
                <li>الاستبعاد الخلفي (Backward Elimination)</li>
                <li>طريقة LASSO</li>
                <li>طريقة Ridge Regression</li>
                <li>طريقة Elastic Net</li>
            </ul>
        </li>
        <li>النمذجة الأوتوماتيكية (Automatic Modeling)</li>
        <li>تحليل التحكم (Control Analysis)</li>
        <li>خوارزميات الغابة العشوائية (Random Forest Algorithms)</li>
        <li>خوارزميات الفروقات (Difference Algorithms)</li>
        <li>خوارزميات اختيار المتغير للتعلم العميق (Variable Selection for Deep Learning)</li>
        <li>خوارزميات التصنيف قبل النمذجة (Classification Algorithms)</li>
    </ul>
    </div>

    <h3 class="section-header">طرق تقييم أهمية المتغيرات:</h3>
    <div class="model-box">
    <ul>
        <li>قيمة المعامل ومعنويته الإحصائية (Coefficient magnitude and significance)</li>
        <li>مقاييس الأهمية النسبية (Measures of relative importance):
            <ul>
                <li>تجزئة R² (R² decomposition)</li>
                <li>تحليل الحساسية (Sensitivity analysis)</li>
                <li>معاملات المرونة (Elasticity coefficients)</li>
            </ul>
        </li>
        <li>أهمية المتغير في نماذج التعلم الآلي:
            <ul>
                <li>أهمية Gini (Gini importance)</li>
                <li>أهمية Permutation (Permutation importance)</li>
                <li>قيم Shapley (Shapley values)</li>
            </ul>
        </li>
        <li>تحليل المكونات الرئيسية (Principal Component Analysis - PCA)</li>
        <li>تحليل العوامل (Factor Analysis)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# إنشاء رسم بياني يوضح عملية اختيار المتغيرات
	var_selection_steps = [
		"تحديد المتغيرات المحتملة بناءً على النظرية",
		"فحص البيانات وإعدادها",
		"تطبيق خوارزميات اختيار المتغيرات",
		"تقييم أهمية المتغيرات",
		"اختبار النموذج مع المتغيرات المختارة",
		"التحقق من استقرار النتائج",
		"تفسير دور المتغيرات المختارة"
	]

	st.plotly_chart(create_process_flow(var_selection_steps), use_container_width=True)

	# إنشاء رسم بياني لطرق اختيار المتغيرات
	variable_selection_methods = [
		"طرق اختيار المتغيرات",
		"الطرق الإحصائية التقليدية", "طرق التعلم الآلي", "طرق التعلم العميق", "الطرق الهجينة"
	]

	traditional_methods = [
		"الطرق الإحصائية التقليدية",
		"الانحدار التدريجي", "اختبارات المعنوية", "معايير المعلومات", "تحليل المكونات الرئيسية"
	]

	machine_learning_methods = [
		"طرق التعلم الآلي",
		"الغابة العشوائية", "LASSO", "Ridge Regression", "Elastic Net", "Gradient Boosting"
	]

	# عرض مخطط طرق اختيار المتغيرات
	st.plotly_chart(create_model_hierarchy("طرق اختيار المتغيرات", variable_selection_methods),
					use_container_width=True)

	# عرض مخطط الطرق الإحصائية التقليدية
	st.plotly_chart(create_model_hierarchy("الطرق الإحصائية التقليدية", traditional_methods), use_container_width=True)

	# عرض مخطط طرق التعلم الآلي
	st.plotly_chart(create_model_hierarchy("طرق التعلم الآلي", machine_learning_methods), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">اعتبارات مهمة عند اختيار المتغيرات:</h3>
    <div class="model-box">
    <ul>
        <li>الأساس النظري: يجب أن يكون هناك مبرر نظري لإدراج المتغير في النموذج.</li>
        <li>تجنب الارتباط المتعدد: يجب تجنب إدراج متغيرات مرتبطة بشكل كبير فيما بينها.</li>
        <li>مشكلة الأبعاد العالية: عندما يكون عدد المتغيرات كبيراً مقارنة بعدد المشاهدات.</li>
        <li>توازن النموذج: النموذج يجب أن يكون بسيطاً بما يكفي للتفسير ومعقداً بما يكفي للدقة.</li>
        <li>اختبار الاستقرار: يجب أن تكون نتائج النموذج مستقرة عبر العينات المختلفة.</li>
        <li>التحيز في اختيار المتغيرات: تجنب التحيز الناتج عن اختيار المتغيرات بناءً على النتائج.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

elif page == "إشكالية السببية":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية السببية</h2>

    <p>
    تعتبر إشكالية السببية من أهم وأصعب الإشكاليات في الدراسات القياسية، حيث تتعلق بتحديد ما إذا كان هناك علاقة سببية بين المتغيرات وليس مجرد ارتباط. الارتباط بين متغيرين لا يعني بالضرورة وجود علاقة سببية، ولذلك تم تطوير عدة منهجيات لاختبار وتحليل العلاقات السببية.
    </p>

    <h3 class="section-header">أنواع السببية:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# إنشاء مخطط لأنواع السببية
	causality_types = [
		"السببية",
		"السببية الإحصائية", "السببية الهندسية"
	]

	statistical_causality = [
		"السببية الإحصائية",
		"سببية غرانجر", "سببية سيمز", "سببية بيرل", "سببية روبن", "سببية المتغيرات الأداتية"
	]

	# عرض مخطط أنواع السببية
	st.plotly_chart(create_model_hierarchy("السببية", causality_types), use_container_width=True)

	# عرض مخطط أنواع السببية الإحصائية
	st.plotly_chart(create_model_hierarchy("السببية الإحصائية", statistical_causality), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">منهجيات واختبارات السببية:</h3>

    <h4>1. اختبارات السببية:</h4>
    <div class="model-box">
    <ul>
        <li>اختبار غرانجر للسببية (Granger Causality Test):
            <ul>
                <li>يختبر ما إذا كان متغير ما يساعد في التنبؤ بمتغير آخر</li>
                <li>يعتمد على نماذج VAR أو VECM</li>
            </ul>
        </li>
        <li>اختبار سيمز للسببية (Sims Causality Test)</li>
        <li>اختبار تودا-يامامتو (Toda-Yamamoto Test):
            <ul>
                <li>يتغلب على مشكلة استقرارية السلاسل الزمنية</li>
            </ul>
        </li>
        <li>اختبار السببية غير الخطية (Nonlinear Causality Test)</li>
        <li>اختبار السببية في المدى الطويل والقصير</li>
    </ul>
    </div>

    <h4>2. نماذج السببية:</h4>
    <div class="model-box">
    <ul>
        <li>نماذج الرسوم البيانية الموجهة غير الدورية (Directed Acyclic Graph - DAG):
            <ul>
                <li>تمثل العلاقات السببية بين المتغيرات بشكل بياني</li>
                <li>تسمح بتحديد المسارات السببية المباشرة وغير المباشرة</li>
            </ul>
        </li>
        <li>نماذج الشبكة (Network Model):
            <ul>
                <li>تمثيل العلاقات بين المتغيرات على شكل شبكة</li>
                <li>تسمح بتحليل تدفق التأثيرات عبر الشبكة</li>
            </ul>
        </li>
        <li>نماذج المعادلات البنائية (Structural Equation Models - SEM):
            <ul>
                <li>تجمع بين نماذج القياس ونماذج العلاقات السببية</li>
            </ul>
        </li>
        <li>نماذج الاستدلال السببي (Causal Inference Models):
            <ul>
                <li>Causal Impact Model</li>
                <li>Causal VAR</li>
                <li>Causal ARIMA</li>
            </ul>
        </li>
    </ul>
    </div>

    <h4>3. طرق التحليل السببي:</h4>
    <div class="model-box">
    <ul>
        <li>طريقة المتغيرات الأداتية (Instrumental Variables):
            <ul>
                <li>تستخدم متغيراً أداتياً مرتبطاً بالمتغير المستقل وليس له تأثير مباشر على المتغير التابع</li>
            </ul>
        </li>
        <li>طريقة الفروق في الفروق (Difference-in-Differences):
            <ul>
                <li>تقارن التغييرات في النتائج بين مجموعتين قبل وبعد معالجة</li>
            </ul>
        </li>
        <li>طريقة الانقطاع في الانحدار (Regression Discontinuity Design):
            <ul>
                <li>تستغل وجود عتبة تحدد المعالجة</li>
            </ul>
        </li>
        <li>طريقة المطابقة (Matching Methods):
            <ul>
                <li>تقارن بين وحدات متشابهة باستثناء المعالجة</li>
            </ul>
        </li>
        <li>نماذج التأثير المتوسط للمعالجة (Average Treatment Effect Models)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)


	# إنشاء رسم بياني للعلاقة السببية
	def create_causality_diagram():
		# إنشاء بيانات المخطط
		nodes = ['X', 'Y', 'Z', 'W']
		edges = [('X', 'Y'), ('Z', 'X'), ('Z', 'Y'), ('W', 'Z')]

		G = nx.DiGraph()
		G.add_nodes_from(nodes)
		G.add_edges_from(edges)

		pos = {'X': (0.3, 0.5), 'Y': (0.7, 0.5), 'Z': (0.5, 0.8), 'W': (0.5, 1.0)}

		edge_x = []
		edge_y = []
		for edge in G.edges():
			x0, y0 = pos[edge[0]]
			x1, y1 = pos[edge[1]]
			edge_x.extend([x0, x1, None])
			edge_y.extend([y0, y1, None])

		edge_trace = go.Scatter(
			x=edge_x, y=edge_y,
			line=dict(width=2, color='#888'),
			hoverinfo='none',
			mode='lines',
			name='العلاقات'
		)

		node_x = []
		node_y = []
		node_text = []
		node_colors = ['#FF9671', '#FFC75F', '#F9F871', '#D65DB1']

		for i, node in enumerate(G.nodes()):
			x, y = pos[node]
			node_x.append(x)
			node_y.append(y)
			if node == 'X':
				node_text.append('X (متغير مستقل)')
			elif node == 'Y':
				node_text.append('Y (متغير تابع)')
			elif node == 'Z':
				node_text.append('Z (متغير وسيط)')
			else:
				node_text.append('W (متغير أداتي)')

		node_trace = go.Scatter(
			x=node_x, y=node_y,
			mode='markers+text',
			text=node_text,
			textposition="top center",
			marker=dict(
				showscale=False,
				color=node_colors,
				size=30,
				line_width=2
			),
			name='المتغيرات'
		)

		# إضافة تسميات للروابط
		annotations = []
		for edge in G.edges():
			x0, y0 = pos[edge[0]]
			x1, y1 = pos[edge[1]]
			annotations.append(dict(
				x=(x0 + x1) / 2,
				y=(y0 + y1) / 2,
				xref="x",
				yref="y",
				text="تأثير",
				showarrow=True,
				arrowhead=2,
				ax=0,
				ay=-30
			))

		fig = go.Figure(data=[edge_trace, node_trace],
						layout=go.Layout(
							title="<b>مثال على العلاقات السببية بين المتغيرات</b>",
							titlefont_size=16,
							showlegend=False,
							hovermode='closest',
							margin=dict(b=20, l=5, r=5, t=40),
							annotations=annotations,
							xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
							yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.4, 1.1]),
							height=500,
							plot_bgcolor='rgba(0,0,0,0)'
						))

		return fig


	# عرض مخطط العلاقة السببية
	st.plotly_chart(create_causality_diagram(), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">خطوات تحليل السببية:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط خطوات تحليل السببية
	causality_steps = [
		"صياغة فرضية السببية بناءً على النظرية",
		"تحديد المنهجية المناسبة للتحليل السببي",
		"اختيار البيانات المناسبة وإعدادها",
		"تطبيق اختبارات السببية المناسبة",
		"تقدير النموذج السببي",
		"تقييم النتائج وتفسيرها",
		"إجراء تحليل الحساسية للتحقق من متانة النتائج"
	]

	st.plotly_chart(create_process_flow(causality_steps), use_container_width=True)

elif page == "إشكالية الفعالية":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية الفعالية</h2>

    <p>
    تتعلق إشكالية الفعالية بقياس وتقييم أثر السياسات أو التدخلات أو البرامج على المتغيرات الاقتصادية أو الاجتماعية. الهدف هو تحديد ما إذا كانت السياسة أو التدخل فعالاً في تحقيق أهدافه المرجوة، وقياس حجم هذا التأثير.
    </p>

    <h3 class="section-header">منهجيات قياس الفعالية:</h3>
    <div class="model-box">
    <ul>
        <li>طرق المنهج شبه التجريبي (Quasi-experimental Methods):
            <ul>
                <li>الفروق في الفروق (Difference-in-Differences)</li>
                <li>الانقطاع في الانحدار (Regression Discontinuity Design)</li>
                <li>المتغيرات الأداتية (Instrumental Variables)</li>
                <li>طرق المطابقة (Matching Methods)، مثل Propensity Score Matching</li>
            </ul>
        </li>
        <li>طرق الاستدلال السببي (Causal Inference Methods):
            <ul>
                <li>نماذج تأثير المعالجة (Treatment Effect Models)</li>
                <li>نماذج Rubin Causal Model</li>
                <li>نماذج Potential Outcomes Framework</li>
            </ul>
        </li>
        <li>أدوات التحليل المضاد (Counterfactual Analysis Tools):
            <ul>
                <li>نماذج المحاكاة (Simulation Models)</li>
                <li>تحليل السيناريوهات (Scenario Analysis)</li>
                <li>نماذج التوازن العام المحسوبة (Computable General Equilibrium Models)</li>
            </ul>
        </li>
    </ul>
    </div>

    <h3 class="section-header">مؤشرات قياس الفعالية:</h3>
    <div class="model-box">
    <ul>
        <li>مؤشرات التأثير المباشر (Direct Impact Indicators):
            <ul>
                <li>متوسط تأثير المعالجة (Average Treatment Effect - ATE)</li>
                <li>متوسط تأثير المعالجة على المعالجين (Average Treatment Effect on the Treated - ATT)</li>
                <li>التأثير الحدي للمعالجة (Marginal Treatment Effect - MTE)</li>
            </ul>
        </li>
        <li>مؤشرات الكفاءة (Efficiency Indicators):
            <ul>
                <li>تحليل التكلفة والعائد (Cost-Benefit Analysis)</li>
                <li>تحليل التكلفة والفعالية (Cost-Effectiveness Analysis)</li>
                <li>معدل العائد الداخلي (Internal Rate of Return)</li>
            </ul>
        </li>
        <li>مؤشرات الفعالية على المدى الطويل (Long-term Effectiveness Indicators):
            <ul>
                <li>استدامة التأثير (Impact Sustainability)</li>
                <li>تأثيرات الانتشار (Spillover Effects)</li>
                <li>التأثيرات غير المباشرة (Indirect Effects)</li>
            </ul>
        </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)


	# إنشاء رسم بياني لطرق قياس الفعالية
	def create_effectiveness_methods_chart():
		methods = ['الفروق في الفروق', 'الانقطاع في الانحدار', 'المتغيرات الأداتية', 'طرق المطابقة',
				   'تحليل السيناريوهات']
		complexity = [7, 8, 9, 6, 5]
		robustness = [8, 9, 7, 6, 4]
		applicability = [9, 7, 6, 8, 9]

		fig = go.Figure()

		fig.add_trace(go.Bar(
			x=methods,
			y=complexity,
			name='التعقيد',
			marker_color='indianred'
		))

		fig.add_trace(go.Bar(
			x=methods,
			y=robustness,
			name='المتانة',
			marker_color='lightsalmon'
		))

		fig.add_trace(go.Bar(
			x=methods,
			y=applicability,
			name='قابلية التطبيق',
			marker_color='lightseagreen'
		))

		fig.update_layout(
			title="<b>مقارنة بين طرق قياس الفعالية</b>",
			xaxis_title="الطريقة",
			yaxis_title="التقييم (1-10)",
			barmode='group',
			height=500,
			font=dict(
				family="Arial",
				size=14
			)
		)

		return fig


	# عرض مخطط طرق قياس الفعالية
	st.plotly_chart(create_effectiveness_methods_chart(), use_container_width=True)


	# إنشاء رسم بياني لمثال على تحليل الفروق في الفروق
	def create_diff_in_diff_chart():
		# إنشاء بيانات افتراضية
		time = list(range(1, 11))
		treated_before = [5, 5.2, 5.4, 5.5, 5.7]
		treated_after = [5.9, 6.5, 7.0, 7.5, 8.0]
		control_before = [5.1, 5.3, 5.5, 5.6, 5.8]
		control_after = [5.9, 6.1, 6.3, 6.5, 6.7]

		intervention_time = 5.5

		fig = go.Figure()

		# إضافة المجموعة المعالجة
		fig.add_trace(go.Scatter(
			x=time[:5],
			y=treated_before,
			mode='lines+markers',
			name='المجموعة المعالجة (قبل)',
			line=dict(color='royalblue')
		))

		fig.add_trace(go.Scatter(
			x=time[5:],
			y=treated_after,
			mode='lines+markers',
			name='المجموعة المعالجة (بعد)',
			line=dict(color='royalblue', dash='dash')
		))

		# إضافة المجموعة الضابطة
		fig.add_trace(go.Scatter(
			x=time[:5],
			y=control_before,
			mode='lines+markers',
			name='المجموعة الضابطة (قبل)',
			line=dict(color='firebrick')
		))

		fig.add_trace(go.Scatter(
			x=time[5:],
			y=control_after,
			mode='lines+markers',
			name='المجموعة الضابطة (بعد)',
			line=dict(color='firebrick', dash='dash')
		))

		# إضافة خط التدخل
		fig.add_shape(
			type="line",
			x0=intervention_time,
			y0=0,
			x1=intervention_time,
			y1=10,
			line=dict(
				color="green",
				width=2,
				dash="dashdot",
			)
		)

		fig.add_annotation(
			x=intervention_time,
			y=9,
			text="وقت التدخل",
			showarrow=True,
			arrowhead=1,
			arrowcolor="green",
			arrowwidth=2,
			ax=-50,
			ay=0
		)

		# إضافة التأثير (الفرق في الفروق)
		fig.add_annotation(
			x=8,
			y=7.5,
			text="التأثير = (Treated After - Treated Before) - (Control After - Control Before)",
			showarrow=True,
			arrowhead=1,
			arrowcolor="purple",
			arrowwidth=2,
			ax=0,
			ay=-40
		)

		fig.update_layout(
			title="<b>مثال على تحليل الفروق في الفروق</b>",
			xaxis_title="الزمن",
			yaxis_title="القيمة",
			height=500,
			font=dict(
				family="Arial",
				size=14
			)
		)

		return fig


	# عرض مخطط مثال على تحليل الفروق في الفروق
	st.plotly_chart(create_diff_in_diff_chart(), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">خطوات تقييم فعالية السياسات أو التدخلات:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط خطوات تقييم الفعالية
	effectiveness_steps = [
		"تحديد السياسة أو التدخل المراد تقييمه",
		"تحديد مؤشرات النتائج المستهدفة",
		"اختيار المنهجية المناسبة لقياس الفعالية",
		"تصميم استراتيجية التعريف (Identification Strategy)",
		"جمع البيانات المناسبة",
		"تطبيق النموذج وتقدير التأثير",
		"تحليل الحساسية والمتانة",
		"تفسير النتائج واستخلاص التوصيات"
	]

	st.plotly_chart(create_process_flow(effectiveness_steps), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">تحديات قياس الفعالية:</h3>
    <div class="model-box">
    <ul>
        <li>مشكلة الانتقائية (Selection Bias): عدم عشوائية اختيار المجموعات المعالجة والضابطة.</li>
        <li>تأثيرات الانتشار (Spillover Effects): تأثر المجموعة الضابطة بالمعالجة.</li>
        <li>مشكلة المتغيرات المحذوفة (Omitted Variable Bias): عدم تضمين متغيرات مؤثرة في النموذج.</li>
        <li>مشكلة الاتجاهات المشتركة (Common Trends Assumption): افتراض تشابه اتجاهات المجموعتين في غياب المعالجة.</li>
        <li>مشكلة التوقيت (Timing Issues): تحديد الفترة المناسبة لقياس التأثير.</li>
        <li>مشكلة الخارجية (External Validity): إمكانية تعميم النتائج على سياقات أخرى.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

elif page == "إشكالية التنبؤ":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية التنبؤ</h2>

    <p>
    تتعلق إشكالية التنبؤ بالقدرة على التوقع بالقيم المستقبلية للمتغيرات بناءً على البيانات التاريخية والنماذج الإحصائية والقياسية. تعتبر عملية التنبؤ من أهم تطبيقات الدراسات القياسية وتستخدم في مجالات متنوعة مثل الاقتصاد والمالية والأعمال وغيرها.
    </p>

    <h3 class="section-header">أنواع نماذج التنبؤ:</h3>
    <div class="model-box">
    <ol>
        <li>الطرق التقليدية (Traditional Methods):
            <ul>
                <li>التمهيد الأسي (Exponential Smoothing)</li>
                <li>نماذج ARIMA (Autoregressive Integrated Moving Average)</li>
                <li>التنبؤ المشروط بالانحدار (Conditional Forecasting)</li>
                <li>نماذج ARCH (Autoregressive Conditional Heteroskedasticity)</li>
                <li>نماذج GARCH (Generalized Autoregressive Conditional Heteroskedasticity)</li>
            </ul>
        </li>
        <li>الطرق الحديثة (Modern Methods):
            <ul>
                <li>خوارزميات الذكاء الاصطناعي (Artificial Intelligence Algorithms):
                    <ul>
                        <li>الشبكات العصبية التلافيفية (CNN - Convolutional Neural Networks)</li>
                        <li>الشبكات العصبية ذات الذاكرة قصيرة-طويلة المدى (LSTM - Long Short-Term Memory)</li>
                        <li>الشبكات العصبية المتكررة (RNN - Recurrent Neural Networks)</li>
                        <li>نماذج CARD (Combined ARIMA and Deep Learning)</li>
                        <li>طريقة TETA (Temporal and Exogenous Trend Analysis)</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>الطرق الحديثة المدمجة (Hybrid Modern Methods):
            <ul>
                <li>نماذج GARCH-LSTM</li>
                <li>نماذج Deep VAR</li>
                <li>نماذج ANN-ARIMA</li>
                <li>نماذج DL-ARIMA</li>
            </ul>
        </li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# إنشاء رسم بياني لأنواع نماذج التنبؤ
	forecasting_models = [
		"نماذج التنبؤ",
		"الطرق التقليدية", "الطرق الحديثة", "الطرق الحديثة المدمجة"
	]

	traditional_models = [
		"الطرق التقليدية",
		"التمهيد الأسي", "نماذج ARIMA", "التنبؤ المشروط بالانحدار", "نماذج ARCH/GARCH"
	]

	modern_models = [
		"الطرق الحديثة",
		"الشبكات العصبية CNN", "الشبكات العصبية LSTM", "الشبكات العصبية RNN", "نماذج CARD", "طريقة TETA"
	]

	hybrid_models = [
		"الطرق الحديثة المدمجة",
		"نماذج GARCH-LSTM", "نماذج Deep VAR", "نماذج ANN-ARIMA", "نماذج DL-ARIMA"
	]

	# عرض مخطط أنواع نماذج التنبؤ
	st.plotly_chart(create_model_hierarchy("نماذج التنبؤ", forecasting_models), use_container_width=True)

	# عرض مخطط الطرق التقليدية
	st.plotly_chart(create_model_hierarchy("الطرق التقليدية", traditional_models), use_container_width=True)

	# عرض مخطط الطرق الحديثة
	st.plotly_chart(create_model_hierarchy("الطرق الحديثة", modern_models), use_container_width=True)


	# إنشاء رسم بياني لمقارنة دقة نماذج التنبؤ
	def create_forecast_accuracy_chart():
		models = ['ARIMA', 'GARCH', 'LSTM', 'CNN', 'GARCH-LSTM', 'Deep VAR']
		mae = [0.42, 0.38, 0.31, 0.33, 0.28, 0.26]
		mse = [0.53, 0.47, 0.39, 0.41, 0.35, 0.33]
		mape = [0.38, 0.35, 0.29, 0.30, 0.25, 0.24]

		fig = go.Figure()

		fig.add_trace(go.Bar(
			x=models,
			y=mae,
			name='MAE (متوسط الخطأ المطلق)',
			marker_color='indianred'
		))

		fig.add_trace(go.Bar(
			x=models,
			y=mse,
			name='MSE (متوسط مربع الخطأ)',
			marker_color='lightsalmon'
		))

		fig.add_trace(go.Bar(
			x=models,
			y=mape,
			name='MAPE (متوسط النسبة المئوية للخطأ المطلق)',
			marker_color='lightseagreen'
		))

		fig.update_layout(
			title="<b>مقارنة دقة نماذج التنبؤ المختلفة</b>",
			xaxis_title="النموذج",
			yaxis_title="قيمة الخطأ (أقل = أفضل)",
			barmode='group',
			height=500,
			font=dict(
				family="Arial",
				size=14
			)
		)

		return fig


	# عرض مخطط مقارنة دقة نماذج التنبؤ
	st.plotly_chart(create_forecast_accuracy_chart(), use_container_width=True)


	# إنشاء رسم بياني لمثال على التنبؤ
	def create_forecast_example_chart():
		# إنشاء بيانات افتراضية
		time_historical = list(range(1, 21))
		time_forecast = list(range(21, 31))

		# القيم التاريخية
		values_historical = [10 + i + 2 * np.sin(i / 2) + np.random.normal(0, 1) for i in range(20)]

		# القيم المتنبأ بها مع فاصل الثقة
		values_forecast = [30 + i + 2 * np.sin(i / 2) for i in range(10)]
		values_forecast_upper = [v + 2 + 0.2 * i for i, v in enumerate(values_forecast)]
		values_forecast_lower = [v - 2 - 0.2 * i for i, v in enumerate(values_forecast)]

		fig = go.Figure()

		# إضافة القيم التاريخية
		fig.add_trace(go.Scatter(
			x=time_historical,
			y=values_historical,
			mode='lines+markers',
			name='القيم التاريخية',
			line=dict(color='royalblue')
		))

		# إضافة القيم المتنبأ بها
		fig.add_trace(go.Scatter(
			x=time_forecast,
			y=values_forecast,
			mode='lines+markers',
			name='القيم المتنبأ بها',
			line=dict(color='firebrick')
		))

		# إضافة فاصل الثقة
		fig.add_trace(go.Scatter(
			x=time_forecast + time_forecast[::-1],
			y=values_forecast_upper + values_forecast_lower[::-1],
			fill='toself',
			fillcolor='rgba(231,107,243,0.2)',
			line=dict(color='rgba(255,255,255,0)'),
			showlegend=True,
			name='فاصل الثقة (95%)'
		))

		# إضافة خط الفصل بين البيانات التاريخية والتنبؤات
		fig.add_shape(
			type="line",
			x0=20.5,
			y0=0,
			x1=20.5,
			y1=50,
			line=dict(
				color="green",
				width=2,
				dash="dashdot",
			)
		)

		fig.add_annotation(
			x=20.5,
			y=45,
			text="بداية التنبؤ",
			showarrow=True,
			arrowhead=1,
			arrowcolor="green",
			arrowwidth=2,
			ax=-50,
			ay=0
		)

		fig.update_layout(
			title="<b>مثال على التنبؤ مع فاصل الثقة</b>",
			xaxis_title="الزمن",
			yaxis_title="القيمة",
			height=500,
			font=dict(
				family="Arial",
				size=14
			)
		)

		return fig


	# عرض مخطط مثال على التنبؤ
	st.plotly_chart(create_forecast_example_chart(), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">مقاييس دقة التنبؤ:</h3>
    <div class="model-box">
    <ul>
        <li>متوسط الخطأ المطلق (MAE - Mean Absolute Error)</li>
        <li>متوسط مربع الخطأ (MSE - Mean Squared Error)</li>
        <li>الجذر التربيعي لمتوسط مربع الخطأ (RMSE - Root Mean Squared Error)</li>
        <li>متوسط النسبة المئوية للخطأ المطلق (MAPE - Mean Absolute Percentage Error)</li>
        <li>معامل ثيل للعدم التساوي (Theil's U)</li>
        <li>معيار المعلومات البيزي (BIC - Bayesian Information Criterion)</li>
        <li>معيار معلومات أكايكي (AIC - Akaike Information Criterion)</li>
    </ul>
    </div>

    <h3 class="section-header">خطوات بناء نموذج للتنبؤ:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط خطوات بناء نموذج التنبؤ
	forecasting_steps = [
		"تحديد الهدف من التنبؤ",
		"تحليل البيانات التاريخية",
		"تقسيم البيانات (تدريب، اختبار، تحقق)",
		"اختيار النموذج المناسب",
		"تقدير النموذج",
		"تقييم دقة النموذج",
		"استخدام النموذج للتنبؤ",
		"مراقبة أداء النموذج وتحديثه"
	]

	st.plotly_chart(create_process_flow(forecasting_steps), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">تحديات التنبؤ:</h3>
    <div class="model-box">
    <ul>
        <li>التعامل مع البيانات غير المستقرة (Non-stationary data)</li>
        <li>التعامل مع تغير الهيكل (Structural changes)</li>
        <li>التعامل مع التقلبات الموسمية والدورية (Seasonal and cyclical variations)</li>
        <li>التعامل مع الأحداث غير المتوقعة (Unexpected events)</li>
        <li>تحديد أفق التنبؤ المناسب (Appropriate forecast horizon)</li>
        <li>اختيار النموذج المناسب بين نماذج متعددة (Model selection)</li>
        <li>تقدير فواصل الثقة للتنبؤات (Confidence intervals for forecasts)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

elif page == "إشكالية الأجل الطويل والأجل القصير":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">إشكالية الأجل الطويل والأجل القصير</h2>

    <p>
    تتعلق إشكالية الأجل الطويل والأجل القصير بدراسة وتحليل العلاقات بين المتغيرات في آفاق زمنية مختلفة. غالباً ما تختلف العلاقات بين المتغيرات في الأجل القصير عنها في الأجل الطويل، مما يتطلب استخدام منهجيات خاصة للتمييز بين هذه العلاقات وتحليلها.
    </p>

    <h3 class="section-header">اختبارات الأجل القصير والمتوسط والطويل:</h3>
    <div class="model-box">
    <ul>
        <li>اختبارات التكامل المشترك (Cointegration Tests):
            <ul>
                <li>اختبار إنجل-غرانجر (Engle-Granger Test)</li>
                <li>اختبار جوهانسن (Johansen Test)</li>
                <li>اختبار الحدود (ARDL Bounds Test)</li>
            </ul>
        </li>
        <li>اختبارات جذر الوحدة (Unit Root Tests):
            <ul>
                <li>اختبار ديكي-فولر الموسع (ADF - Augmented Dickey-Fuller)</li>
                <li>اختبار فيليبس-بيرون (PP - Phillips-Perron)</li>
                <li>اختبار KPSS</li>
            </ul>
        </li>
        <li>اختبارات الاستقرار الهيكلي (Structural Stability Tests):
            <ul>
                <li>اختبار CUSUM</li>
                <li>اختبار CUSUMSQ</li>
                <li>اختبار شاو (Chow Test)</li>
            </ul>
        </li>
    </ul>
    </div>

    <h3 class="section-header">النماذج المستخدمة في تحليل العلاقات في الأجل الطويل والقصير:</h3>
    <div class="model-box">
    <ul>
        <li>نماذج تصحيح الخطأ (ECM - Error Correction Models):
            <ul>
                <li>تجمع بين ديناميكيات الأجل القصير والعلاقات طويلة الأجل</li>
                <li>تقيس سرعة التعديل نحو التوازن طويل الأجل</li>
            </ul>
        </li>
        <li>نماذج الانحدار الذاتي ذو الفجوات الموزعة (ARDL - Autoregressive Distributed Lag):
            <ul>
                <li>تسمح بتقدير العلاقات في الأجل القصير والطويل في آن واحد</li>
                <li>تتعامل مع متغيرات ذات درجات تكامل مختلفة</li>
            </ul>
        </li>
        <li>نماذج متجه تصحيح الخطأ (VECM - Vector Error Correction Models):
            <ul>
                <li>امتداد لنماذج ECM للتعامل مع متغيرات متعددة</li>
                <li>تحليل العلاقات المتبادلة في الأجل القصير والطويل</li>
            </ul>
        </li>
        <li>نماذج التحول الهيكلي (Structural Break Models):
            <ul>
                <li>تتعامل مع التغيرات في العلاقات عبر الزمن</li>
                <li>تسمح بتحديد نقاط التحول في العلاقات طويلة الأجل</li>
            </ul>
        </li>
        <li>نماذج العتبة (Threshold Models):
            <ul>
                <li>تسمح بتغير العلاقات عند تجاوز قيم معينة (عتبات)</li>
                <li>مناسبة للعلاقات غير الخطية عبر الزمن</li>
            </ul>
        </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)


	# إنشاء رسم بياني لمثال على العلاقة بين الأجل القصير والطويل
	def create_short_long_term_chart():
		# إنشاء بيانات افتراضية
		time = list(range(1, 101))
		y_long_term = [0.5 * t for t in time]
		y_short_term = [0.5 * t + 5 * np.sin(t / 5) for t in time]

		fig = go.Figure()

		# إضافة العلاقة طويلة الأجل
		fig.add_trace(go.Scatter(
			x=time,
			y=y_long_term,
			mode='lines',
			name='العلاقة طويلة الأجل',
			line=dict(color='royalblue', width=3)
		))

		# إضافة العلاقة قصيرة الأجل
		fig.add_trace(go.Scatter(
			x=time,
			y=y_short_term,
			mode='lines',
			name='العلاقة قصيرة الأجل',
			line=dict(color='firebrick', width=1.5)
		))

		# إضافة توضيح للانحرافات قصيرة الأجل
		for i in range(10, 90, 20):
			if y_short_term[i] > y_long_term[i]:
				arrow_y = 5
			else:
				arrow_y = -5

			fig.add_annotation(
				x=time[i],
				y=y_short_term[i],
				text="انحراف قصير الأجل",
				showarrow=True,
				arrowhead=1,
				arrowcolor="green",
				arrowwidth=2,
				ax=0,
				ay=arrow_y
			)

		# إضافة توضيح للعلاقة طويلة الأجل
		fig.add_annotation(
			x=80,
			y=y_long_term[80],
			text="اتجاه طويل الأجل",
			showarrow=True,
			arrowhead=1,
			arrowcolor="blue",
			arrowwidth=2,
			ax=-80,
			ay=0
		)

		fig.update_layout(
			title="<b>مثال على العلاقة بين الأجل القصير والأجل الطويل</b>",
			xaxis_title="الزمن",
			yaxis_title="القيمة",
			height=500,
			font=dict(
				family="Arial",
				size=14
			)
		)

		return fig


	# عرض مخطط مثال على العلاقة بين الأجل القصير والطويل
	st.plotly_chart(create_short_long_term_chart(), use_container_width=True)


	# إنشاء رسم بياني لنموذج تصحيح الخطأ
	def create_ecm_chart():
		# إنشاء بيانات افتراضية
		time = list(range(1, 51))
		equilibrium = [2 * t for t in time]

		# حدث صدمة في الفترة 20
		actual = []
		for t in range(50):
			if t < 20:
				actual.append(equilibrium[t] + np.random.normal(0, 3))
			elif t == 20:
				actual.append(equilibrium[t] + 30)  # صدمة كبيرة
			else:
				adjustment = 0.2 * (equilibrium[t - 1] - actual[t - 1])  # معامل تصحيح الخطأ
				actual.append(actual[t - 1] + adjustment + np.random.normal(0, 3))

		fig = go.Figure()

		# إضافة التوازن طويل الأجل
		fig.add_trace(go.Scatter(
			x=time,
			y=equilibrium,
			mode='lines',
			name='التوازن طويل الأجل',
			line=dict(color='royalblue', width=3)
		))

		# إضافة القيم الفعلية
		fig.add_trace(go.Scatter(
			x=time,
			y=actual,
			mode='lines',
			name='القيم الفعلية',
			line=dict(color='firebrick', width=1.5)
		))

		# إضافة توضيح للصدمة
		fig.add_annotation(
			x=time[20],
			y=actual[20],
			text="صدمة",
			showarrow=True,
			arrowhead=1,
			arrowcolor="red",
			arrowwidth=2,
			ax=0,
			ay=-40
		)

		# إضافة توضيح لعملية التصحيح
		fig.add_annotation(
			x=time[35],
			y=actual[35],
			text="عملية تصحيح الخطأ",
			showarrow=True,
			arrowhead=1,
			arrowcolor="green",
			arrowwidth=2,
			ax=0,
			ay=30
		)

		fig.update_layout(
			title="<b>مثال على نموذج تصحيح الخطأ (ECM)</b>",
			xaxis_title="الزمن",
			yaxis_title="القيمة",
			height=500,
			font=dict(
				family="Arial",
				size=14
			)
		)

		return fig


	# عرض مخطط نموذج تصحيح الخطأ
	st.plotly_chart(create_ecm_chart(), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">خطوات تحليل العلاقات في الأجل الطويل والقصير:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط خطوات تحليل العلاقات
	time_horizon_steps = [
		"اختبار استقرارية السلاسل الزمنية",
		"تحديد درجة التكامل للمتغيرات",
		"اختبار وجود علاقة توازنية طويلة الأجل (تكامل مشترك)",
		"اختيار النموذج المناسب (ECM, ARDL, VECM...)",
		"تقدير العلاقات في الأجل القصير والطويل",
		"تحليل سرعة التعديل نحو التوازن طويل الأجل",
		"اختبار استقرار النموذج",
		"تفسير النتائج واستخلاص الاستنتاجات"
	]

	st.plotly_chart(create_process_flow(time_horizon_steps), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">مفاهيم أساسية في تحليل الأجل الطويل والقصير:</h3>
    <div class="model-box">
    <ul>
        <li>التكامل المشترك (Cointegration): وجود علاقة توازنية طويلة الأجل بين متغيرات غير مستقرة.</li>
        <li>آلية تصحيح الخطأ (Error Correction Mechanism): العملية التي تعيد المتغيرات إلى التوازن طويل الأجل بعد الصدمات.</li>
        <li>سرعة التعديل (Speed of Adjustment): معدل عودة النظام إلى التوازن طويل الأجل بعد الصدمات.</li>
        <li>الاستجابة الديناميكية (Dynamic Response): كيفية استجابة المتغيرات للصدمات عبر الزمن.</li>
        <li>دوال الاستجابة للصدمات (Impulse Response Functions): تتبع أثر صدمة في متغير على متغيرات أخرى عبر الزمن.</li>
        <li>تحليل التباين (Variance Decomposition): تحديد نسبة التباين في متغير ناتجة عن صدمات في متغيرات أخرى.</li>
    </ul>
    </div>

    <h3 class="section-header">تحديات تحليل الأجل الطويل والقصير:</h3>
    <div class="model-box">
    <ul>
        <li>التمييز بين الاتجاهات العشوائية والاتجاهات المحددة.</li>
        <li>التعامل مع التغيرات الهيكلية في العلاقات طويلة الأجل.</li>
        <li>تحديد الفترات الزمنية المناسبة لتحليل الأجل القصير والمتوسط والطويل.</li>
        <li>التعامل مع العلاقات غير الخطية في الأجل القصير والطويل.</li>
        <li>اختيار طول الفجوات المناسب في النماذج الديناميكية.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

elif page == "الإشكالية المدمجة":
	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h2 class="sub-header">الإشكالية المدمجة</h2>

    <p>
    تتعلق الإشكالية المدمجة بالدراسات التي تتضمن تحليل عدة إشكاليات في آن واحد، مثل دراسة العلاقات السببية والتنبؤ في آن واحد، أو دراسة المحددات والتأثير طويل الأجل معاً. تتطلب هذه الإشكالية استخدام منهجيات متطورة تجمع بين عدة نماذج أو تقنيات.
    </p>

    <h3 class="section-header">أنواع الإشكاليات المدمجة:</h3>
    <div class="model-box">
    <ul>
        <li>الإشكالية المدمجة بين الأثر والسببية</li>
        <li>الإشكالية المدمجة بين المحددات والتنبؤ</li>
        <li>الإشكالية المدمجة بين الأجل الطويل والفعالية</li>
        <li>الإشكالية المدمجة بين المقارنة والتأثير</li>
        <li>الإشكالية المدمجة متعددة الأبعاد</li>
    </ul>
    </div>

    <h3 class="section-header">منهجيات التعامل مع الإشكاليات المدمجة:</h3>
    <div class="model-box">
    <ol>
        <li>النماذج متعددة الأبعاد (Multidimensional Models):
            <ul>
                <li>نماذج العوامل الديناميكية (DFM - Dynamic Factor Models)</li>
                <li>نماذج متجه الانحدار الذاتي العالمية (GVAR - Global VAR)</li>
                <li>نماذج الشبكات (Network Models)</li>
            </ul>
        </li>
        <li>منهجيات الدمج (Integration Methodologies):
            <ul>
                <li>الدمج المتسلسل (Sequential Integration): تطبيق عدة منهجيات بشكل متتالي</li>
                <li>الدمج المتوازي (Parallel Integration): تطبيق عدة منهجيات بشكل متواز ثم دمج النتائج</li>
                <li>الدمج الهرمي (Hierarchical Integration): تطبيق منهجيات على مستويات مختلفة من التحليل</li>
            </ul>
        </li>
        <li>نماذج تأثير الانتشار (Spillover Effect Models):
            <ul>
                <li>نماذج تحليل الانتشار (Spillover Analysis)</li>
                <li>نماذج نقل العدوى (Contagion Models)</li>
                <li>نماذج الانتشار الشبكي (Network Diffusion Models)</li>
            </ul>
        </li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)


	# إنشاء رسم بياني للإشكاليات المدمجة
	def create_integrated_issues_chart():
		# إنشاء بيانات المخطط
		issues = [
			"إشكالية الأثر والتأثير", "إشكالية المقارنة", "إشكالية المحددات",
			"إشكالية السببية", "إشكالية الفعالية", "إشكالية التنبؤ",
			"إشكالية الأجل الطويل والأجل القصير"
		]

		integrated_issues = [
			"الإشكالية المدمجة بين الأثر والسببية",
			"الإشكالية المدمجة بين المحددات والتنبؤ",
			"الإشكالية المدمجة بين الأجل الطويل والفعالية",
			"الإشكالية المدمجة بين المقارنة والتأثير",
			"الإشكالية المدمجة متعددة الأبعاد"
		]

		# إنشاء المصفوفة لتحديد العلاقات
		matrix = np.zeros((len(issues), len(integrated_issues)))

		# تعيين العلاقات بين الإشكاليات الأساسية والمدمجة
		matrix[0, 0] = 1  # الأثر والسببية
		matrix[3, 0] = 1

		matrix[2, 1] = 1  # المحددات والتنبؤ
		matrix[5, 1] = 1

		matrix[6, 2] = 1  # الأجل الطويل والفعالية
		matrix[4, 2] = 1

		matrix[1, 3] = 1  # المقارنة والتأثير
		matrix[0, 3] = 1

		# الإشكالية متعددة الأبعاد تشمل الجميع
		for i in range(len(issues)):
			matrix[i, 4] = 0.5

		fig = go.Figure(data=go.Heatmap(
			z=matrix,
			x=integrated_issues,
			y=issues,
			colorscale='YlGnBu',
			showscale=False,
			hoverongaps=False
		))

		fig.update_layout(
			title="<b>العلاقات بين الإشكاليات الأساسية والإشكاليات المدمجة</b>",
			height=500,
			font=dict(
				family="Arial",
				size=14
			),
			margin=dict(l=10, r=10, t=50, b=10)
		)

		return fig


	# عرض مخطط الإشكاليات المدمجة
	st.plotly_chart(create_integrated_issues_chart(), use_container_width=True)


	# إنشاء رسم بياني لنموذج شبكي متعدد الأبعاد
	def create_network_model_chart():
		# إنشاء بيانات المخطط
		G = nx.DiGraph()

		# إضافة العقد
		countries = ["دولة A", "دولة B", "دولة C", "دولة D", "دولة E"]
		sectors = ["قطاع مالي", "قطاع صناعي", "قطاع خدمي"]

		# إضافة العقد للدول والقطاعات
		for country in countries:
			G.add_node(country, type="country")

		for sector in sectors:
			G.add_node(sector, type="sector")

		# إضافة الروابط بين الدول
		G.add_edge("دولة A", "دولة B", weight=0.7)
		G.add_edge("دولة A", "دولة C", weight=0.5)
		G.add_edge("دولة B", "دولة D", weight=0.6)
		G.add_edge("دولة C", "دولة E", weight=0.4)
		G.add_edge("دولة D", "دولة E", weight=0.8)

		# إضافة الروابط بين الدول والقطاعات
		G.add_edge("دولة A", "قطاع مالي", weight=0.9)
		G.add_edge("دولة B", "قطاع صناعي", weight=0.8)
		G.add_edge("دولة C", "قطاع خدمي", weight=0.7)
		G.add_edge("دولة D", "قطاع مالي", weight=0.6)
		G.add_edge("دولة E", "قطاع صناعي", weight=0.5)

		# إضافة الروابط بين القطاعات
		G.add_edge("قطاع مالي", "قطاع صناعي", weight=0.4)
		G.add_edge("قطاع صناعي", "قطاع خدمي", weight=0.3)

		# استخدام خوارزمية تخطيط spring_layout لتحديد مواقع العقد
		pos = nx.spring_layout(G, seed=42)

		# إنشاء قوائم للرسم
		edge_x = []
		edge_y = []
		edge_weights = []

		for edge in G.edges(data=True):
			x0, y0 = pos[edge[0]]
			x1, y1 = pos[edge[1]]
			edge_x.extend([x0, x1, None])
			edge_y.extend([y0, y1, None])
			edge_weights.append(edge[2]['weight'])

		edge_trace = go.Scatter(
			x=edge_x, y=edge_y,
			line=dict(width=1, color='#888'),
			hoverinfo='none',
			mode='lines')

		node_x = []
		node_y = []
		node_text = []
		node_colors = []
		node_sizes = []

		for node in G.nodes(data=True):
			x, y = pos[node[0]]
			node_x.append(x)
			node_y.append(y)
			node_text.append(node[0])

			if node[1]['type'] == "country":
				node_colors.append('#FF9671')
				node_sizes.append(20)
			else:
				node_colors.append('#6495ED')
				node_sizes.append(15)

		node_trace = go.Scatter(
			x=node_x, y=node_y,
			mode='markers+text',
			text=node_text,
			textposition="top center",
			marker=dict(
				showscale=False,
				color=node_colors,
				size=node_sizes,
				line_width=2))

		fig = go.Figure(data=[edge_trace, node_trace],
						layout=go.Layout(
							title="<b>مثال على نموذج شبكي متعدد الأبعاد (دول وقطاعات)</b>",
							titlefont_size=16,
							showlegend=False,
							hovermode='closest',
							margin=dict(b=20, l=5, r=5, t=40),
							xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
							yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
							height=500,
							plot_bgcolor='rgba(0,0,0,0)'
						))

		return fig


	# عرض مخطط النموذج الشبكي متعدد الأبعاد
	st.plotly_chart(create_network_model_chart(), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">خطوات التعامل مع الإشكاليات المدمجة:</h3>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

	# عرض مخطط خطوات التعامل مع الإشكاليات المدمجة
	integrated_steps = [
		"تحديد الإشكاليات المختلفة التي تتضمنها الدراسة",
		"تحليل العلاقات والتفاعلات بين الإشكاليات",
		"اختيار المنهجية المناسبة للتعامل مع الإشكاليات المدمجة",
		"تحديد تسلسل التحليل أو هيكلية الدمج",
		"جمع وإعداد البيانات المناسبة",
		"تطبيق النماذج والتقنيات المختلفة",
		"دمج النتائج وتحليلها بشكل متكامل",
		"استخلاص الاستنتاجات والتوصيات"
	]

	st.plotly_chart(create_process_flow(integrated_steps), use_container_width=True)

	st.markdown('<div class="rtl">', unsafe_allow_html=True)
	st.markdown("""
    <h3 class="section-header">أمثلة على الإشكاليات المدمجة:</h3>
    <div class="model-box">
    <ol>
        <li>دراسة تأثير السياسة النقدية على النمو الاقتصادي:
            <ul>
                <li>إشكالية الأثر والتأثير: قياس تأثير السياسة النقدية على النمو</li>
                <li>إشكالية الأجل الطويل والقصير: تحليل الآثار في الأجل القصير والطويل</li>
                <li>إشكالية الفعالية: تقييم فعالية السياسة النقدية في تحقيق أهدافها</li>
            </ul>
        </li>
        <li>دراسة العلاقات التجارية بين الدول:
            <ul>
                <li>إشكالية المقارنة: مقارنة التدفقات التجارية بين الدول</li>
                <li>إشكالية السببية: تحديد اتجاه السببية في العلاقات التجارية</li>
                <li>إشكالية التنبؤ: التنبؤ بتطور العلاقات التجارية المستقبلية</li>
            </ul>
        </li>
        <li>تحليل أزمة مالية عالمية:
            <ul>
                <li>إشكالية المحددات: تحديد أسباب وعوامل الأزمة</li>
                <li>إشكالية تأثير الانتشار: دراسة انتشار الأزمة عبر الدول والقطاعات</li>
                <li>إشكالية الفعالية: تقييم فعالية سياسات الاستجابة للأزمة</li>
            </ul>
        </li>
    </ol>
    </div>

    <h3 class="section-header">تحديات التعامل مع الإشكاليات المدمجة:</h3>
    <div class="model-box">
    <ul>
        <li>تعقيد النماذج والمنهجيات المستخدمة</li>
        <li>صعوبة جمع وإعداد البيانات المناسبة لكل إشكالية</li>
        <li>التعامل مع العلاقات المتداخلة بين الإشكاليات</li>
        <li>صعوبة تفسير النتائج بشكل متكامل</li>
        <li>الحاجة إلى معرفة واسعة بمختلف المنهجيات والنماذج</li>
        <li>التوازن بين العمق والشمولية في التحليل</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
	st.markdown('</div>', unsafe_allow_html=True)

# إضافة التذييل
st.markdown("""
<style>
.footer {
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #F5F5F5;
    color: #1E3D59;
    text-align: center;
    padding: 10px;
    margin-top: 50px;
    border-radius: 10px;
}
</style>
<div class="footer">
    <p>© 2025 مخطط معالجة الإشكاليات في الدراسات القياسية - الدكتور مروان رودان</p>
</div>
""", unsafe_allow_html=True)