هذا التطبيق مبني باستخدام Streamlit ويعمل كدليل تفاعلي للباحثين في مجالات الاقتصاد والمالية والعلوم الاجتماعية. يهدف التطبيق إلى توضيح الإشكاليات القياسية الشائعة واقتراح النماذج والمنهجيات المناسبة لمعالجتها. يتم تقديم التطبيق باللغة العربية ويتميز بتخطيط يدعم الاتجاه من اليمين إلى اليسار (RTL).

This Streamlit application, titled "مخطط معالجة الإشكاليات في الدراسات القياسية" (Diagram for Addressing Problematics in Econometric Studies), serves as an interactive guide for researchers in economics, finance, and social sciences. It aims to clarify common econometric problematics and suggest appropriate models and methodologies for addressing them. The application is presented in Arabic and features a right-to-left (RTL) layout.

## الميزات (Features)

*   **التنقل عبر الشريط الجانبي (Sidebar Navigation):** سهولة التنقل بين الإشكاليات القياسية المختلفة.
*   **صفحة النظرة العامة (Overview Page):** تقدم مقدمة عامة ومخطط شبكي يوضح العلاقات بين الإشكاليات.
*   **صفحات مخصصة للإشكاليات (Dedicated Problematics Pages):** لكل إشكالية (الأثر والتأثير، المقارنة، المحددات، السببية، الفعالية، التنبؤ، الأجل الطويل والقصير، الإشكالية المدمجة) صفحة خاصة بها تحتوي على:
    *   شروحات مفصلة.
    *   قوائم بالنماذج والمنهجيات ذات الصلة.
    *   وسائل بصرية مساعدة مثل المخططات الشجرية (Treemaps) لهيكلية النماذج، ومخططات تدفق العمليات (Process Flow Diagrams)، ومخططات أمثلة (مثل مخططات السببية، مخططات الفروق في الفروق).
*   **تصورات بيانية تفاعلية (Interactive Visualizations):** استخدام مكتبة Plotly لإنشاء مخططات ديناميكية وغنية بالمعلومات.
*   **تنسيق CSS مخصص (Custom CSS):** يضمن عرضًا صحيحًا للغة العربية من اليمين إلى اليسار وتنسيقًا محسنًا لتجربة المستخدم.
*   **ملاحظات إرشادية (Informative Notes):** يتضمن الشريط الجانبي ملاحظات هامة للباحثين.
*   **تذييل (Footer):** يشير إلى مطور المحتوى.

## المتطلبات الأساسية (Prerequisites)

*   Python (يفضل إصدار 3.7 أو أحدث)
*   المكتبات المذكورة في ملف `requirements.txt`:
    *   streamlit
    *   plotly
    *   pandas
    *   numpy
    *   networkx
