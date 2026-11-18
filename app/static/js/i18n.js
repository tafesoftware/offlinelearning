(() => {
  const isAmharic = document.documentElement.lang === 'am';
  const translations = {
    'Offline LMS': 'ከመስመር ውጭ የትምህርት ስርዓት',
    'Learning System for Rural & Remote Schools': 'የገጠር እና ሩቅ ትምህርት ቤቶች የመማሪያ ስርዓት',
    '• Learning System for Rural & Remote Schools': '• የገጠር እና ሩቅ ትምህርት ቤቶች የመማሪያ ስርዓት',
    'Designed for zero-bandwidth classrooms, solar-powered labs, and sneakernet sync.': 'የኢንተርኔት ግንኙነት ለሌላቸው ክፍሎች፣ በፀሐይ ኃይል ለሚሰሩ ላቦራቶሪዎች እና ከመስመር ውጭ የመረጃ ማመሳሰል የተዘጋጀ።',
    'Offline-First Learning for Rural & Remote Schools': 'ለገጠር እና ሩቅ ትምህርት ቤቶች ከመስመር ውጭ ቅድሚያ የሚሰጥ ትምህርት',
    'Install Offline App:': 'ከመስመር ውጭ መተግበሪያን ይጫኑ:',
    'Learn anytime without internet!': 'ያለ ኢንተርኔት በማንኛውም ጊዜ ይማሩ!',
    'Install App': 'መተግበሪያን ይጫኑ',
    'Language': 'ቋንቋ',
    'Ethiopian Ministry of Education logo': 'የኢትዮጵያ ትምህርት ሚኒስቴር አርማ',
    'Home': 'መነሻ',
    'Contact Us': 'ያግኙን',
    'Location': 'አድራሻ',
    'About System': 'ስለ ስርዓቱ',
    'Textbooks (9–12)': 'የመማሪያ መጻሕፍት (9–12)',
    '📚 Textbooks (9–12)': '📚 የመማሪያ መጻሕፍት (9–12)',
    'Teacher Hub': 'የመምህራን ማዕከል',
    'Gradebook': 'የውጤት መዝገብ',
    'Sneakernet & Sync': 'የመረጃ ማመሳሰል',
    'My Courses': 'የእኔ ትምህርቶች',
    'Offline Hub': 'ከመስመር ውጭ ማዕከል',
    'Logout': 'ውጣ',
    'Login': 'ይግቡ',
    'Register': 'ይመዝገቡ',
    'Sign In': 'ይግቡ',
    'Create an account': 'መለያ ይፍጠሩ',
    'Create an Account': 'መለያ ይፍጠሩ',
    'Register / ይመዝገቡ': 'ይመዝገቡ',
    'Home / መነሻ': 'መነሻ',
    'Contact Us / ያግኙን': 'ያግኙን',
    'Location / አድራሻ': 'አድራሻ',
    'About System / ስለ ስርዓቱ': 'ስለ ስርዓቱ',
    'Textbooks (9–12) / የመማሪያ መጻሕፍት': 'የመማሪያ መጻሕፍት (9–12)',
    'Teacher Hub / የመምህራን ማዕከል': 'የመምህራን ማዕከል',
    'Gradebook / የውጤት መዝገብ': 'የውጤት መዝገብ',
    'Sneakernet & Sync / የመረጃ ማመሳሰል': 'የመረጃ ማመሳሰል',
    'My Courses / የእኔ ትምህርቶች': 'የእኔ ትምህርቶች',
    'Offline Hub / ከመስመር ውጭ ማዕከል': 'ከመስመር ውጭ ማዕከል',
    'Logout / ውጣ': 'ውጣ',
    'Login / ይግቡ': 'ይግቡ',
    'Welcome to': 'እንኳን ወደ',
    'Access lessons, textbooks, and quizzes through your school\'s local learning system, even when internet access is unavailable.': 'ኢንተርኔት ባይኖርም በትምህርት ቤትዎ የአካባቢ የመማሪያ ስርዓት ትምህርቶችን፣ መጻሕፍትን እና ፈተናዎችን ይጠቀሙ።',
    'Go to Dashboard': 'ወደ ዳሽቦርድ ይሂዱ',
    'Learn offline': 'ከመስመር ውጭ ይማሩ',
    'Open lessons and take quizzes using your school\'s local network.': 'የትምህርት ቤትዎን አካባቢያዊ ኔትወርክ በመጠቀም ትምህርቶችን ይክፈቱ እና ፈተናዎችን ይውሰዱ።',
    'Explore textbooks': 'መማሪያ መጻሕፍትን ይመልከቱ',
    'Find available digital learning materials in the textbook library.': 'በመማሪያ መጽሐፍት ቤተ-መጻሕፍት ውስጥ ያሉ ዲጂታል የመማሪያ መሳሪያዎችን ያግኙ።',
    'Stay in sync': 'ተመሳስለው ይቆዩ',
    'Learning progress can sync when devices reconnect to the school hub.': 'መሳሪያዎች ከትምህርት ቤቱ ማዕከል ጋር እንደገና ሲገናኙ የትምህርት እድገት ሊመሳሰል ይችላል።',
    'Welcome to Offline LMS': 'እንኳን ወደ ከመስመር ውጭ የትምህርት ስርዓት በደህና መጡ',
    'Home - Offline LMS': 'መነሻ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Student Dashboard - Offline LMS': 'የተማሪ ዳሽቦርድ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Teacher Hub - Offline LMS': 'የመምህራን ማዕከል - ከመስመር ውጭ የትምህርት ስርዓት',
    'Sign In - Offline LMS': 'ይግቡ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Register / ይመዝገቡ - Offline LMS': 'ይመዝገቡ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Contact Us - Offline LMS': 'ያግኙን - ከመስመር ውጭ የትምህርት ስርዓት',
    'Location - Offline LMS': 'አድራሻ - ከመስመር ውጭ የትምህርት ስርዓት',
    'For help with accounts, courses, or classroom access, contact your teacher or school administrator.': 'ስለ መለያዎች፣ ኮርሶች ወይም የክፍል መዳረሻ እገዛ ከፈለጉ መምህርዎን ወይም የትምህርት ቤቱን አስተዳዳሪ ያነጋግሩ።',
    'This installation does not have an email address or phone number configured.': 'ይህ ስርዓት የኢሜይል አድራሻ ወይም ስልክ ቁጥር አልተዋቀረለትም።',
    'The LMS runs locally at your school, so support is provided by your school team.': 'ይህ የመማሪያ ስርዓት በትምህርት ቤትዎ አካባቢ ይሰራል፤ ስለዚህ ድጋፍ በትምህርት ቤትዎ ቡድን ይሰጣል።',
    'School information configured for this Offline LMS installation:': 'ለዚህ የመማሪያ ስርዓት የተዋቀረ የትምህርት ቤት መረጃ:',
    'School:': 'ትምህርት ቤት:',
    'District:': 'ወረዳ:',
    'Not configured': 'አልተዋቀረም',
    'A physical street address has not been configured. Ask your school administrator for directions.': 'የትምህርት ቤቱ የመንገድ አድራሻ አልተዋቀረም። አቅጣጫ ለማግኘት የትምህርት ቤቱን አስተዳዳሪ ይጠይቁ።',
    'Offline LMS is an offline-first learning platform for rural and remote schools.': 'ከመስመር ውጭ የትምህርት ስርዓት ለገጠር እና ሩቅ ትምህርት ቤቶች የተዘጋጀ ከመስመር ውጭ ቅድሚያ የሚሰጥ የመማሪያ መድረክ ነው።',
    'Students can access lessons, textbooks, and quizzes on the school\'s local network.': 'ተማሪዎች በትምህርት ቤቱ አካባቢያዊ ኔትወርክ ትምህርቶችን፣ መጻሕፍትን እና ፈተናዎችን ማግኘት ይችላሉ።',
    'Learning activity can be saved offline and synchronized when devices reconnect.': 'የትምህርት እንቅስቃሴ ከመስመር ውጭ ሊቀመጥ እና መሳሪያዎች እንደገና ሲገናኙ ሊመሳሰል ይችላል።',
    'Teachers can manage courses, review progress, and exchange curriculum using local sync tools.': 'መምህራን ኮርሶችን ማስተዳደር፣ እድገትን መከታተል እና የትምህርት ይዘትን በአካባቢያዊ ማመሳሰል መሳሪያዎች መለዋወጥ ይችላሉ።',
    'Home /': 'መነሻ /',
    'Create Local Account / አዲስ መለያ ይፍጠሩ': 'አዲስ መለያ ይፍጠሩ',
    'Register to study or manage offline courses / ለመማር ወይም ከመስመር ውጭ ትምህርቶችን ለማስተዳደር ይመዝገቡ': 'ለመማር ወይም ከመስመር ውጭ ትምህርቶችን ለማስተዳደር ይመዝገቡ',
    'e.g. Samuel / ለምሳሌ: Samuel': 'ለምሳሌ: Samuel',
    'e.g. Kiptoo / ለምሳሌ: Kiptoo': 'ለምሳሌ: Kiptoo',
    'e.g. samuel_k / ለምሳሌ: samuel_k': 'ለምሳሌ: samuel_k',
    'e.g. Environmental Science & Sanitation': 'ለምሳሌ፡ የአካባቢ ሳይንስ እና ንጽህና',
    'e.g. SCI-501': 'ለምሳሌ፡ SCI-501',
    'e.g. Clean Water and Filtration Methods': 'ለምሳሌ፡ ንጹህ ውሃ እና የማጣሪያ ዘዴዎች',
    'One or two sentences highlighting the core concept (read aloud by the audio reader)...': 'ዋናውን ሀሳብ የሚያብራሩ አንድ ወይም ሁለት ዓረፍተ ነገሮች ይጻፉ...',
    '# Introduction\n\nWrite the lesson notes and step-by-step instructions here...': '# መግቢያ\n\nየትምህርቱን ማስታወሻዎች እና ደረጃ በደረጃ መመሪያዎችን እዚህ ይጻፉ...',
    'e.g. Water Filtration Comprehension Check': 'ለምሳሌ፡ የውሃ ማጣራት ግንዛቤ ምርመራ',
    'e.g. Ethiopian Grade 10 Chemistry Student Textbook': 'ለምሳሌ፡ የኢትዮጵያ 10ኛ ክፍል ኬሚስትሪ መማሪያ መጽሐፍ',
    'e.g. CHEM-10': 'ለምሳሌ፡ CHEM-10',
    'Ministry of Education (MoE) Ethiopia': 'የኢትዮጵያ ትምህርት ሚኒስቴር (MoE)',
    'First Step': 'የመጀመሪያ እርምጃ',
    'Completed first lesson': 'የመጀመሪያውን ትምህርት አጠናቋል',
    'Bookworm': 'መጽሐፍ አፍቃሪ',
    'Completed 5 lessons': '5 ትምህርቶችን አጠናቋል',
    'Quiz Master': 'የፈተና ባለሙያ',
    'Passed 3 quizzes': '3 ፈተናዎችን አልፏል',
    'Offline Scholar': 'ከመስመር ውጭ ተማሪ',
    'Prepared for offline study': 'ከመስመር ውጭ ለማጥናት ተዘጋጅቷል',
    'Remove': 'አስወግድ',
    'Secondary Form 1': 'ሁለተኛ ደረጃ 1',
    'All Levels': 'ሁሉም ደረጃዎች',
    'Student / ተማሪ': 'ተማሪ',
    'Teacher / መምህር': 'መምህር',
    'Grade / ክፍል': 'ክፍል',
    'Grade 5 / 5ኛ ክፍል': '5ኛ ክፍል',
    'Grade 6 / 6ኛ ክፍል': '6ኛ ክፍል',
    'Grade 7 / 7ኛ ክፍል': '7ኛ ክፍል',
    'Grade 8 / 8ኛ ክፍል': '8ኛ ክፍል',
    'Grade 9 / 9ኛ ክፍል': '9ኛ ክፍል',
    'Grade 10 / 10ኛ ክፍል': '10ኛ ክፍል',
    'Grade 11 / 11ኛ ክፍል': '11ኛ ክፍል',
    'Grade 12 / 12ኛ ክፍል': '12ኛ ክፍል',
    'Choose a field / ዘርፍ ይምረጡ': 'ዘርፍ ይምረጡ',
    'Natural Science / ተፈጥሮ ሳይንስ': 'ተፈጥሮ ሳይንስ',
    'Social Science / ማህበራዊ ሳይንስ': 'ማህበራዊ ሳይንስ',
    'Create a password / የይለፍ ቃል ይፍጠሩ': 'የይለፍ ቃል ይፍጠሩ',
    'Complete Registration / ምዝገባውን ያጠናቅቁ': 'ምዝገባውን ያጠናቅቁ',
    'Already have an account? / መለያ አለዎት?': 'መለያ አለዎት?',
    'Sign In / ይግቡ': 'ይግቡ',
    'Rural & Remote School Learning System': 'የገጠር እና ሩቅ ትምህርት ቤቶች የመማሪያ ስርዓት',
    'Username or Student ID': 'የተጠቃሚ ስም ወይም የተማሪ መለያ ቁጥር',
    'Enter username or ID': 'የተጠቃሚ ስም ወይም መለያ ቁጥር ያስገቡ',
    'Password / PIN': 'የይለፍ ቃል / ፒን',
    'Enter password': 'የይለፍ ቃል ያስገቡ',
    'New student or teacher?': 'አዲስ ተማሪ ወይም መምህር ነዎት?',
    'Hello,': 'ሰላም፣',
    'Enrolled in': 'የተመዘገቡት በ',
    '• Completed': '• ተጠናቋል',
    'Completed': 'ተጠናቋል',
    'lessons': 'ትምህርቶች',
    'Download Lessons for Home Study': 'ለቤት ጥናት ትምህርቶችን ያውርዱ',
    'Learning Achievements & Badges': 'የትምህርት ስኬቶች እና ሽልማቶች',
    'Your Subjects': 'የእርስዎ ትምህርቶች',
    'Done': 'ተጠናቋል',
    'Core rural curriculum modules and interactive quizzes.': 'የገጠር ዋና የትምህርት ሞጁሎች እና ተሳታፊ ፈተናዎች።',
    'Lessons Completed': 'የተጠናቀቁ ትምህርቶች',
    'Lessons': 'ትምህርቶች',
    'Open Subject →': 'ትምህርቱን ይክፈቱ →',
    'Open Subject &rarr;': 'ትምህርቱን ይክፈቱ →',
    'No subjects currently available. Ask your teacher to import the curriculum pack.': 'በአሁኑ ጊዜ ምንም ትምህርቶች አይገኙም። መምህርዎን የትምህርት ይዘቱን እንዲያስገቡ ይጠይቁ።',
    'Recent Quiz Results': 'የቅርብ ጊዜ የፈተና ውጤቶች',
    'Quiz': 'ፈተና',
    'Subject': 'ትምህርት',
    'Score': 'ውጤት',
    'Result': 'ውጤት',
    'Sync Mode': 'የማመሳሰል ሁኔታ',
    'Passed': 'አልፏል',
    'Needs Review': 'ግምገማ ያስፈልገዋል',
    'Offline Synced': 'ከመስመር ውጭ ተመሳስሏል',
    'Direct Hub': 'ቀጥታ ከማዕከሉ',
    'Submitted offline, synced via sneakernet/LAN': 'ከመስመር ውጭ ቀርቦ በsneakernet/LAN ተመሳስሏል',
    'Taken offline at home, synced via hub/sneakernet': 'በቤት ከመስመር ውጭ ተወስዶ በማዕከል/sneakernet ተመሳስሏል',
    'Back to Dashboard': 'ወደ ዳሽቦርድ ተመለስ',
    'Back to Teacher Hub': 'ወደ መምህራን ማዕከል ተመለስ',
    'Back to Textbook Library': 'ወደ መማሪያ መጻሕፍት ቤተ-መጻሕፍት ተመለስ',
    'Back to': 'ወደ ተመለስ',
    'Add Lesson': 'ትምህርት ጨምር',
    'Add Quiz': 'ፈተና ጨምር',
    'Course Lessons': 'የኮርስ ትምህርቶች',
    'Lesson Title': 'የትምህርት ርዕስ',
    'Est. Time': 'ግምታዊ ጊዜ',
    'Status': 'ሁኔታ',
    'Action': 'ተግባር',
    'Pending': 'በመጠባበቅ ላይ',
    'Start Lesson →': 'ትምህርት ጀምር →',
    'Start Lesson &rarr;': 'ትምህርት ጀምር →',
    'Edit': 'አርትዕ',
    'This subject is listed in the catalog, but its textbook or lessons have not been added yet.': 'ይህ ትምህርት በዝርዝሩ ውስጥ ተካትቷል፣ ነገር ግን መጽሐፉ ወይም ትምህርቶቹ ገና አልተጨመሩም።',
    'Module Tests & Quizzes': 'የሞጁል ፈተናዎች',
    'Questions': 'ጥያቄዎች',
    'Test your knowledge on this module.': 'በዚህ ሞጁል ላይ ያለዎትን እውቀት ይፈትሹ።',
    'Passing Score:': 'ለማለፍ የሚያስፈልግ ውጤት:',
    'Best:': 'ምርጥ:',
    'Not Attempted': 'አልተሞከረም',
    'Retake Quiz': 'ፈተናውን እንደገና ይውሰዱ',
    'Take Quiz': 'ፈተናውን ይውሰዱ',
    'Lesson': 'ትምህርት',
    'mins': 'ደቂቃ',
    'Lesson Completed': 'ትምህርቱ ተጠናቋል',
    'Mark as Completed': 'እንደተጠናቀቀ ምልክት ያድርጉ',
    'Core Concept:': 'ዋና ጽንሰ-ሀሳብ:',
    'Audio Lesson Overview': 'የድምጽ ትምህርት አጠቃላይ እይታ',
    'Listen to teacher summary (ideal for low-light or audio review)': 'የመምህሩን ማጠቃለያ ያዳምጡ',
    '▶ Play Audio Summary': '▶ የድምጽ ማጠቃለያውን ያጫውቱ',
    '⏹ Stop Audio': '⏹ ድምጹን ያቁሙ',
    'Check your understanding:': 'ያለዎትን ግንዛቤ ይፈትሹ:',
    'Complete the lesson quiz to test what you have learned.': 'የተማሩትን ለመፈተሽ የትምህርቱን ፈተና ይውሰዱ።',
    'Take Quiz:': 'ፈተና ይውሰዱ:',
    'Previous:': 'ቀዳሚ:',
    'Next:': 'ቀጣይ:',
    'Finish Module →': 'ሞጁሉን ጨርስ →',
    '← Back to Dashboard': '← ወደ ዳሽቦርድ ተመለስ',
    '← Back to Textbook Library': '← ወደ መማሪያ መጻሕፍት ቤተ-መጻሕፍት ተመለስ',
    'Answer all questions below. Your answers will be graded instantly.': 'ከታች ያሉትን ጥያቄዎች ሁሉ ይመልሱ። መልሶችዎ ወዲያውኑ ይመዘናሉ።',
    'All work is saved locally in offline storage.': 'ሁሉም ስራዎች ከመስመር ውጭ በአካባቢው ይቀመጣሉ።',
    'Submit Quiz': 'ፈተናውን ያስገቡ',
    'Prepare your phone, tablet, or laptop for home study with zero internet.': 'ያለ ኢንተርኔት ለቤት ጥናት ስልክዎን፣ ታብሌትዎን ወይም ላፕቶፕዎን ያዘጋጁ።',
    'Download Curriculum': 'የትምህርት ይዘትን ያውርዱ',
    'Download all lessons, notes, and quiz questions into your browser\'s local memory. You can continue reading and answering quizzes at home completely disconnected.': 'ሁሉንም ትምህርቶች፣ ማስታወሻዎች እና የፈተና ጥያቄዎችን በአሳሽዎ አካባቢያዊ ማህደረ ትውስታ ውስጥ ያውርዱ። ከኢንተርኔት ውጭ ሆነው በቤት ማንበብ እና ፈተና መመለስ ይችላሉ።',
    'Download All Courses for Offline Study': 'ከመስመር ውጭ ለማጥናት ሁሉንም ኮርሶች ያውርዱ',
    'Checking cached courses...': 'የተቀመጡ ኮርሶችን በመፈተሽ ላይ...',
    'Offline Outbox Queue': 'ከመስመር ውጭ የሚጠብቁ ስራዎች',
    'Any quizzes you take or lessons you complete while offline are stored safely on this device. When you bring your device back near the school Wi-Fi or hotspot, tap sync below.': 'ከመስመር ውጭ የወሰዱት ፈተና ወይም ያጠናቀቁት ትምህርት በዚህ መሳሪያ ላይ በደህና ይቀመጣል። መሳሪያውን ወደ ትምህርት ቤቱ Wi-Fi ሲመልሱ ከታች ያለውን ማመሳሰል ይጫኑ።',
    '🔄 Sync Outbox to School Hub Now': '🔄 የሚጠብቁ ስራዎችን አሁን ከትምህርት ቤቱ ማዕከል ጋር ያመሳስሉ',
    'Auto-sync runs automatically whenever connected to the hub.': 'ከማዕከሉ ጋር ሲገናኙ ራስ-ሰር ማመሳሰል ይከናወናል።',
    'Items Pending Upload in Outbox': 'በመላክ ላይ የሚጠብቁ ንጥሎች',
    'Loading outbox records...': 'የሚጠብቁ መዝገቦችን በመጫን ላይ...',
    'How Offline Learning Works in Rural Schools': 'በገጠር ትምህርት ቤቶች ከመስመር ውጭ ትምህርት እንዴት ይሰራል',
    '1. At School (Hub Connected)': '1. በትምህርት ቤት (ከማዕከሉ ጋር ሲገናኝ)',
    'Connect your phone or laptop to the teacher\'s Wi-Fi hotspot. Open Offline LMS and tap "Download All Courses".': 'ስልክዎን ወይም ላፕቶፕዎን ከመምህሩ Wi-Fi ጋር ያገናኙ። የመማሪያ ስርዓቱን ከፍተው "ሁሉንም ኮርሶች ያውርዱ" የሚለውን ይጫኑ።',
    '2. At Home (Zero Internet)': '2. በቤት (ኢንተርኔት ሳይኖር)',
    'Open Offline LMS anytime. Read lessons, take quizzes, and track your streaks. Submissions are saved locally.': 'የመማሪያ ስርዓቱን በማንኛውም ጊዜ ይክፈቱ። ትምህርቶችን ያንብቡ፣ ፈተናዎችን ይውሰዱ እና እድገትዎን ይከታተሉ። መልሶች በአካባቢው ይቀመጣሉ።',
    '3. Return & Sync': '3. ተመልሰው ያመሳስሉ',
    'When back in school, connect to the local Wi-Fi. All your scores and completions sync in seconds!': 'ወደ ትምህርት ቤት ሲመለሱ ከአካባቢያዊው Wi-Fi ጋር ይገናኙ። ውጤቶችዎ እና ያጠናቀቋቸው ትምህርቶች በጥቂት ሰከንዶች ውስጥ ይመሳሰላሉ።',
    'Teacher & School Admin Console': 'የመምህራን እና የትምህርት ቤት አስተዳዳሪ መቆጣጠሪያ',
    'Manage offline curriculum, student progress, and sneakernet synchronization': 'ከመስመር ውጭ የትምህርት ይዘትን፣ የተማሪዎችን እድገት እና የመረጃ ማመሳሰልን ያስተዳድሩ',
    'Add Subject': 'ትምህርት ጨምር',
    'Sneakernet Sync': 'የመረጃ ማመሳሰል',
    'REGISTERED STUDENTS': 'የተመዘገቡ ተማሪዎች',
    'ACTIVE SUBJECTS': 'ንቁ ትምህርቶች',
    'TOTAL LESSONS': 'ጠቅላላ ትምህርቶች',
    'QUIZ SUBMISSIONS': 'የተላኩ ፈተናዎች',
    'Course Subjects & Curriculum': 'የኮርስ ትምህርቶች እና የትምህርት ይዘት',
    'New Subject': 'አዲስ ትምህርት',
    'Code': 'ኮድ',
    'Subject Title': 'የትምህርት ርዕስ',
    'Grade': 'ክፍል',
    'Quizzes': 'ፈተናዎች',
    'Actions': 'ተግባሮች',
    'View': 'ይመልከቱ',
    '+ Lesson': '+ ትምህርት',
    'No subjects created yet. Click "+ New Subject" or import a curriculum pack.': 'ገና ምንም ትምህርቶች አልተፈጠሩም። "+ አዲስ ትምህርት" ይጫኑ ወይም የትምህርት ይዘት ያስገቡ።',
    'Recent Student Quiz Activity': 'የቅርብ ጊዜ የተማሪ ፈተና እንቅስቃሴ',
    'View Full Gradebook →': 'ሙሉ የውጤት መዝገብ ይመልከቱ →',
    'View Full Gradebook &rarr;': 'ሙሉ የውጤት መዝገብ ይመልከቱ →',
    'Student': 'ተማሪ',
    'Origin': 'ምንጭ',
    'Time': 'ጊዜ',
    'Class Gradebook - Offline LMS': 'የክፍል ውጤት መዝገብ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Export Gradebook to USB': 'የውጤት መዝገብን ወደ USB ይላኩ',
    'Student Assessment Gradebook': 'የተማሪ ምዘና ውጤት መዝገብ',
    'Total Records': 'ጠቅላላ መዝገቦች',
    'Student Name': 'የተማሪ ስም',
    'Class / Grade': 'ክፍል',
    'Quiz Title': 'የፈተና ርዕስ',
    'Needs Help': 'እገዛ ያስፈልገዋል',
    'Recorded Time': 'የተመዘገበበት ጊዜ',
    'No student quiz submissions recorded yet. Once students take quizzes, results will appear here.': 'ገና የተማሪዎች የፈተና ውጤቶች አልተመዘገቡም። ተማሪዎች ፈተና ሲወስዱ ውጤቶቹ እዚህ ይታያሉ።',
    'New Subject - Offline LMS': 'አዲስ ትምህርት - ከመስመር ውጭ የትምህርት ስርዓት',
    'Create New Subject': 'አዲስ ትምህርት ይፍጠሩ',
    'Subject Code (Short Identifier)': 'የትምህርት ኮድ (አጭር መለያ)',
    'Grade / Target Level': 'ክፍል / የታለመ ደረጃ',
    'Description & Learning Outcomes': 'መግለጫ እና የትምህርት ውጤቶች',
    'Explain what students will learn in this subject...': 'ተማሪዎች በዚህ ትምህርት ምን እንደሚማሩ ያብራሩ...',
    'Cancel': 'ሰርዝ',
    'Save Subject': 'ትምህርቱን ያስቀምጡ',
    'Create Quiz - Offline LMS': 'ፈተና ይፍጠሩ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Create New Quiz for': 'ለዚህ አዲስ ፈተና ይፍጠሩ:',
    'Attach to Specific Lesson (Optional)': 'ከተወሰነ ትምህርት ጋር ያያይዙ (አማራጭ)',
    '-- General Module Quiz --': '-- አጠቃላይ የሞጁል ፈተና --',
    'Passing Score Percentage': 'ለማለፍ የሚያስፈልግ ውጤት በመቶኛ',
    'Instructions / Description': 'መመሪያዎች / መግለጫ',
    'Short instructions for students...': 'ለተማሪዎች አጭር መመሪያ...',
    'Question Bank': 'የጥያቄ ስብስብ',
    '+ Add Another Question': '+ ሌላ ጥያቄ ጨምር',
    'Question 1': 'ጥያቄ 1',
    'Type the question here...': 'ጥያቄውን እዚህ ይጻፉ...',
    'Option A': 'ምርጫ ሀ',
    'Option B': 'ምርጫ ለ',
    'Option C': 'ምርጫ ሐ',
    'Option D': 'ምርጫ መ',
    'Correct Option': 'ትክክለኛው ምርጫ',
    'Educational Explanation (Shown after grading)': 'ማብራሪያ (ከውጤት በኋላ ይታያል)',
    'Educational Explanation': 'ማብራሪያ',
    'Why this is the correct answer...': 'ይህ መልስ ለምን ትክክል እንደሆነ...',
    'Save Quiz & Questions': 'ፈተናውን እና ጥያቄዎቹን ያስቀምጡ',
    'Sneakernet & Sync Console - Offline LMS': 'የመረጃ ማመሳሰል መቆጣጠሪያ - ከመስመር ውጭ የትምህርት ስርዓት',
    'Sneakernet & Data Sync Console': 'የመረጃ ማመሳሰል መቆጣጠሪያ',
    'Exchange academic records and new curriculum using portable USB thumb drives when internet is unavailable.': 'ኢንተርኔት በሌለበት ጊዜ የትምህርት መዝገቦችን እና አዲስ የትምህርት ይዘትን በUSB ማህደረ ትውስታ ይለዋወጡ።',
    '1. Export School Sync Bundle (USB Outbound)': '1. የትምህርት ቤት ማመሳሰል ፋይል ይላኩ (USB ወደ ውጭ)',
    'Creates a cryptographic JSON bundle containing all student submissions, lesson completions, and attendance logs. Save this file onto a USB flash drive and take it to the district office or closest internet connection.': 'ሁሉንም የተማሪ ምላሾች፣ የተጠናቀቁ ትምህርቶች እና የተገኝነት መዝገቦችን የያዘ የJSON ፋይል ይፈጥራል። ፋይሉን በUSB ላይ ያስቀምጡ እና ወደ ወረዳ ቢሮ ወይም ወደ ቅርብ የኢንተርኔት ግንኙነት ይውሰዱት።',
    'Total Submissions to Export:': 'ለመላክ ጠቅላላ ምላሾች:',
    'from offline student devices': 'ከተማሪዎች ከመስመር ውጭ መሳሪያዎች',
    'Download Sync Bundle to USB (.beacon.json)': 'የማመሳሰል ፋይሉን ወደ USB ያውርዱ (.beacon.json)',
    '2. Import Curriculum Pack (USB Inbound)': '2. የትምህርት ይዘት ፋይል ያስገቡ (USB ወደ ውስጥ)',
    'Load new textbooks, interactive lessons, and quiz banks provided by your district office or Ministry of Education via USB drive.': 'ከወረዳ ቢሮ ወይም ከትምህርት ሚኒስቴር በUSB የተሰጡ አዳዲስ መጻሕፍትን፣ ተሳታፊ ትምህርቶችን እና የፈተና ጥያቄዎችን ያስገቡ።',
    'Select Curriculum Pack File (.json / .pack)': 'የትምህርት ይዘት ፋይል ይምረጡ (.json / .pack)',
    'Import Curriculum Pack to School Server': 'የትምህርት ይዘቱን ወደ ትምህርት ቤቱ ሰርቨር ያስገቡ',
    'Synchronization Audit Trail': 'የማመሳሰል ታሪክ መዝገብ',
    'Logs': 'መዝገቦች',
    'Type': 'አይነት',
    'Items': 'ንጥሎች',
    'Source / Origin': 'ምንጭ',
    'Details': 'ዝርዝሮች',
    'Timestamp': 'የጊዜ ማህተም',
    'USB Export': 'USB ወደ ውጭ መላክ',
    'USB Import': 'USB ከውጭ ማስገባት',
    'Student PWA Sync': 'የተማሪ PWA ማመሳሰል',
    'No sync events recorded yet.': 'ገና ምንም የማመሳሰል ክስተት አልተመዘገበም።',
    'Ethiopian Grade 9-12 Digital Textbook Library - Offline LMS': 'የኢትዮጵያ 9–12ኛ ክፍል ዲጂታል መማሪያ መጻሕፍት - ከመስመር ውጭ የትምህርት ስርዓት',
    'Ministry of Education Ethiopia': 'የኢትዮጵያ ትምህርት ሚኒስቴር',
    'New Revised Curriculum': 'አዲስ የተሻሻለ ሥርዓተ ትምህርት',
    'Grade 9 – 12 Digital Textbook Library': 'የ9–12ኛ ክፍል ዲጂታል መማሪያ መጻሕፍት ቤተ-መጻሕፍት',
    'Browse Ethiopian secondary subjects by grade and stream. Available PDFs and lessons can be read offline; subjects without content are marked.': 'የኢትዮጵያ ሁለተኛ ደረጃ ትምህርቶችን በክፍል እና በዘርፍ ይመልከቱ። ያሉ PDF ፋይሎች እና ትምህርቶች ከመስመር ውጭ ሊነበቡ ይችላሉ።',
    '+ Upload PDF Textbook': '+ PDF መማሪያ መጽሐፍ ይጫኑ',
    'AVAILABLE MATERIALS': 'ያሉ የትምህርት መሳሪያዎች',
    'SECONDARY GRADES': 'ሁለተኛ ደረጃ ክፍሎች',
    'Grades 9, 10, 11 & 12': '9ኛ፣ 10ኛ፣ 11ኛ እና 12ኛ ክፍሎች',
    'OFFLINE ACCESS': 'ከመስመር ውጭ መዳረሻ',
    '100% Zero-Data Ready': '100% ያለ ዳታ ዝግጁ',
    'Select Grade:': 'ክፍል ይምረጡ:',
    'All Grades (9–12)': 'ሁሉም ክፍሎች (9–12)',
    'Grade 9': '9ኛ ክፍል',
    'Grade 10': '10ኛ ክፍል',
    'Grade 11': '11ኛ ክፍል',
    'Grade 12': '12ኛ ክፍል',
    'Stream:': 'ዘርፍ:',
    'All Streams': 'ሁሉም ዘርፎች',
    'Natural Science': 'ተፈጥሮ ሳይንስ',
    'Social Science': 'ማህበራዊ ሳይንስ',
    'Search book by subject or unit...': 'መጽሐፍን በትምህርት ወይም በርዕስ ይፈልጉ...',
    'subjects': 'ትምህርቶች',
    'Core / Common': 'ዋና / የጋራ',
    'Common Subjects': 'የጋራ ትምህርቶች',
    'Publisher:': 'አሳታሚ:',
    'Full PDF uploaded on local server': 'ሙሉ PDF ፋይል በአካባቢያዊ ሰርቨር ተጭኗል',
    'Official PDF': 'ኦፊሴላዊ PDF',
    'Interactive lessons are available': 'ተሳታፊ ትምህርቶች ይገኛሉ',
    'Interactive Reader': 'ተሳታፊ አንባቢ',
    'Textbook and lessons have not been added': 'መጽሐፉ እና ትምህርቶቹ አልተጨመሩም',
    'Subject listing - content not uploaded': 'የትምህርት ዝርዝር - ይዘት አልተጫነም',
    'Read Book': 'መጽሐፉን ያንብቡ',
    'Download': 'ያውርዱ',
    'No textbooks found matching your search criteria.': 'ከፍለጋዎ ጋር የሚዛመድ መማሪያ መጽሐፍ አልተገኘም።',
    'Reset Filters': 'ማጣሪያዎችን ዳግም ያስጀምሩ',
    'Upload Textbook - Ethiopian Digital Library': 'መማሪያ መጽሐፍ ይጫኑ - የኢትዮጵያ ዲጂታል ቤተ-መጻሕፍት',
    'Upload Textbook to School Library': 'መማሪያ መጽሐፍን ወደ ትምህርት ቤቱ ቤተ-መጻሕፍት ይጫኑ',
    'Book Title': 'የመጽሐፍ ርዕስ',
    'Subject Code': 'የትምህርት ኮድ',
    'Grade Level': 'የክፍል ደረጃ',
    'Curriculum Stream': 'የትምህርት ዘርፍ',
    'Common / General Secondary': 'የጋራ / አጠቃላይ ሁለተኛ ደረጃ',
    'Natural Science Stream': 'የተፈጥሮ ሳይንስ ዘርፍ',
    'Social Science Stream': 'የማህበራዊ ሳይንስ ዘርፍ',
    'Publisher / Authority': 'አሳታሚ / ባለስልጣን',
    'Curriculum Units & Overview': 'የሥርዓተ ትምህርት ክፍሎች እና አጠቃላይ እይታ',
    'Outline of units and topics covered according to the Ethiopian New Curriculum...': 'በኢትዮጵያ አዲስ ሥርዓተ ትምህርት መሰረት የሚሸፈኑ ክፍሎችን እና ርዕሶችን ይዘርዝሩ...',
    'Select Textbook PDF File (.pdf)': 'የመማሪያ መጽሐፍ PDF ፋይል ይምረጡ (.pdf)',
    'Upload the official PDF file to store it locally on the school micro-server for offline student downloads.': 'ተማሪዎች ከመስመር ውጭ እንዲያወርዱት ኦፊሴላዊውን PDF ፋይል በትምህርት ቤቱ ሰርቨር ላይ ያስቀምጡ።',
    'Save & Register Book': 'መጽሐፉን ያስቀምጡ እና ይመዝግቡ',
    'FEDERAL DEMOCRATIC REPUBLIC OF ETHIOPIA • MINISTRY OF EDUCATION': 'የኢትዮጵያ ፌዴራላዊ ዴሞክራሲያዊ ሪፐብሊክ • የትምህርት ሚኒስቴር',
    'Download Offline Copy': 'ከመስመር ውጭ ቅጂ ያውርዱ',
    'Curriculum:': 'ሥርዓተ ትምህርት:',
    'Edition:': 'እትም:',
    'Curriculum Overview:': 'የሥርዓተ ትምህርት አጠቃላይ እይታ:',
    'Official PDF Document Reader': 'ኦፊሴላዊ PDF ሰነድ አንባቢ',
    'Open in New Tab ↗': 'በአዲስ ትር ይክፈቱ ↗',
    'Textbook Units & Companion Modules': 'የመጽሐፍ ክፍሎች እና ተያያዥ ሞጁሎች',
    'mins study time': 'ደቂቃ የጥናት ጊዜ',
    'Key Competency Summary:': 'የቁልፍ ብቃት ማጠቃለያ:',
    'Available in offline mode without internet': 'ያለ ኢንተርኔት በከመስመር ውጭ ሁኔታ ይገኛል',
    'Open Full Lesson & Practice Questions →': 'ሙሉ ትምህርቱን እና የልምምድ ጥያቄዎችን ይክፈቱ →',
    'New Lesson': 'አዲስ ትምህርት',
    'Edit Lesson': 'ትምህርት አርትዕ',
    'Lesson Order Number': 'የትምህርት ቅደም ተከተል ቁጥር',
    'Estimated Reading Time (Minutes)': 'ግምታዊ የንባብ ጊዜ (ደቂቃ)',
    'Key Concept / Audio Summary': 'ዋና ሀሳብ / የድምጽ ማጠቃለያ',
    'Lesson Content (Markdown Supported)': 'የትምህርት ይዘት (Markdown ይደገፋል)',
    'Use ## Heading, - bullet points, > notes to organize thoughts clearly for students.': 'ለተማሪዎች ግልጽ እንዲሆን ርዕስ፣ ነጥቦች እና ማስታወሻዎችን ይጠቀሙ።',
    'Save Lesson': 'ትምህርቱን ያስቀምጡ',
    'Lesson marked as completed!': 'ትምህርቱ እንደተጠናቀቀ ተመልክቷል!',
    'Saved offline! Will sync when connected to school hub.': 'ከመስመር ውጭ ተቀምጧል! ከትምህርት ቤቱ ማዕከል ጋር ሲገናኝ ይመሳሰላል።',
    'Could not save completion:': 'ማጠናቀቁን ማስቀመጥ አልተቻለም:',
    'Text-to-speech audio is not supported on this browser.': 'ይህ አሳሽ ጽሑፍን ወደ ድምጽ መቀየር አይደግፍም።',
    'Explanation:': 'ማብራሪያ:',
    'No explanation provided.': 'ምንም ማብራሪያ አልተሰጠም።',
    'Submit (': 'ያስገቡ (',
    ' Answered)': ' ተመልሷል)',
    'Congratulations! You Passed!': 'እንኳን ደስ አለዎት! አልፈዋል!',
    'Good Effort! Keep Practicing!': 'ጥሩ ሙከራ! ልምምድዎን ይቀጥሉ!',
    'Passing required:': 'ለማለፍ የሚያስፈልገው:',
    '✅ Submission synced with school server.': '✅ ምላሹ ከትምህርት ቤቱ ሰርቨር ጋር ተመሳስሏል።',
    '💾 Submission saved securely offline in your device. It will automatically upload when connected to the school hub.': '💾 ምላሹ በመሳሪያዎ ላይ ከመስመር ውጭ በደህና ተቀምጧል። ከትምህርት ቤቱ ማዕከል ጋር ሲገናኝ በራስ-ሰር ይላካል።',
    'Question ': 'ጥያቄ ',
    ' of ': ' ከ ',
    ' Points': ' ነጥቦች',
    'Hub Connected': 'ከማዕከሉ ጋር ተገናኝቷል',
    'Offline Mode': 'ከመስመር ውጭ ሁኔታ',
    'General': 'አጠቃላይ',
    'Please sign in to access this page.': 'ይህን ገጽ ለመጠቀም እባክዎ ይግቡ።',
    'Access restricted to teachers and administrators.': 'መዳረሻው ለመምህራን እና ለአስተዳዳሪዎች ብቻ የተገደበ ነው።',
    'Access restricted to administrators.': 'መዳረሻው ለአስተዳዳሪዎች ብቻ የተገደበ ነው።',
    'Invalid username or password. Please try again.': 'የተጠቃሚ ስም ወይም የይለፍ ቃል ትክክል አይደለም። እባክዎ እንደገና ይሞክሩ።',
    'First name, last name, username and password are required. / የመጀመሪያ ስም፣ የአባት ስም፣ የተጠቃሚ ስም እና የይለፍ ቃል ያስፈልጋሉ።': 'የመጀመሪያ ስም፣ የአባት ስም፣ የተጠቃሚ ስም እና የይለፍ ቃል ያስፈልጋሉ።',
    'Choose a grade before registering. / ከመመዝገብዎ በፊት ክፍል ይምረጡ።': 'ከመመዝገብዎ በፊት ክፍል ይምረጡ።',
    'For Grades 11 and 12, choose Natural Science or Social Science. / ለ11ኛ እና 12ኛ ክፍሎች ተፈጥሮ ሳይንስ ወይም ማህበራዊ ሳይንስ ይምረጡ።': 'ለ11ኛ እና 12ኛ ክፍሎች ተፈጥሮ ሳይንስ ወይም ማህበራዊ ሳይንስ ይምረጡ።',
    'Username already exists. Please choose another. / ይህ የተጠቃሚ ስም አስቀድሞ ተይዟል። እባክዎ ሌላ ይምረጡ።': 'ይህ የተጠቃሚ ስም አስቀድሞ ተይዟል። እባክዎ ሌላ ይምረጡ።',
    'Account registered successfully! Please log in. / ምዝገባዎ በተሳካ ሁኔታ ተጠናቋል። እባክዎ ይግቡ።': 'ምዝገባዎ በተሳካ ሁኔታ ተጠናቋል። እባክዎ ይግቡ።',
    'You have been signed out.': 'ከስርዓቱ ወጥተዋል።',
    'No curriculum pack file was uploaded.': 'የትምህርት ይዘት ፋይል አልተጫነም።',
    'Please select a valid .json or .pack file.': 'ትክክለኛ .json ወይም .pack ፋይል ይምረጡ።',
    'Title and Subject Code are required.': 'የትምህርት ርዕስ እና ኮድ ያስፈልጋሉ።',
    'Subject Code already exists. Please choose a unique code.': 'ይህ የትምህርት ኮድ አስቀድሞ አለ። እባክዎ ሌላ ኮድ ይምረጡ።',
    'Title and Lesson Content are required.': 'የትምህርት ርዕስ እና ይዘት ያስፈልጋሉ።',
    'This subject is listed in the catalog, but its textbook or lessons are not available yet.': 'ይህ ትምህርት በዝርዝሩ ውስጥ ተካትቷል፣ ነገር ግን መጽሐፉ ወይም ትምህርቶቹ ገና አይገኙም።',
    'Book title and subject code are required.': 'የመጽሐፍ ርዕስ እና የትምህርት ኮድ ያስፈልጋሉ።',
    'All subjects downloaded successfully for offline use!': 'ሁሉም ትምህርቶች ከመስመር ውጭ ለመጠቀም በተሳካ ሁኔታ ወርደዋል!',
    'Syncing...': 'በማመሳሰል ላይ...',
    'No courses cached locally yet': 'እስካሁን በአካባቢው የተቀመጡ ኮርሶች የሉም',
    'Waiting for Hub': 'ማዕከሉን በመጠበቅ ላይ',
    'Item Type': 'የንጥል አይነት',
    'Recorded At': 'የተመዘገበበት ጊዜ',
    'Quiz Result': 'የፈተና ውጤት',
    'Lesson Completion': 'የትምህርት ማጠናቀቅ',
    'About System - Offline LMS': 'ስለ ስርዓቱ - ከመስመር ውጭ የትምህርት ስርዓት'
  };

  const registeredText = new WeakSet();

  function stripAmharicSuffix(value) {
    return value.replace(/\s*\/\s*[^/]*[\u1200-\u137F][^/]*$/, '');
  }

  function getTranslation(value) {
    if (translations[value]) return translations[value];

    const dynamicPatterns = [
      [/^Welcome back, (.+)!$/, (_, name) => `እንኳን ደህና መጡ፣ ${name}!`],
      [/^Subject '(.+)' created successfully!$/, (_, title) => `ትምህርቱ "${title}" በተሳካ ሁኔታ ተፈጥሯል!`],
      [/^Lesson '(.+)' created successfully!$/, (_, title) => `ትምህርቱ "${title}" በተሳካ ሁኔታ ተፈጥሯል!`],
      [/^Lesson '(.+)' updated successfully!$/, (_, title) => `ትምህርቱ "${title}" በተሳካ ሁኔታ ተዘምኗል!`],
      [/^Quiz '(.+)' and question bank created!$/, (_, title) => `የ"${title}" ፈተና እና የጥያቄ ስብስብ ተፈጥረዋል!`],
      [/^Question (\d+) of (\d+)$/, (_, current, total) => `ጥያቄ ${current} ከ ${total}`],
      [/^Question (\d+)$/, (_, number) => `ጥያቄ ${number}`],
      [/^(\d+) Total Records$/, (_, count) => `${count} ጠቅላላ መዝገቦች`],
      [/^(\d+) Logs$/, (_, count) => `${count} መዝገቦች`],
      [/^(\d+) Items$/, (_, count) => `${count} ንጥሎች`],
      [/^(\d+) subjects$/, (_, count) => `${count} ትምህርቶች`],
      [/^(\d+) Questions$/, (_, count) => `${count} ጥያቄዎች`],
      [/^(\d+) Lessons$/, (_, count) => `${count} ትምህርቶች`],
      [/^Best: (\d+)%$/, (_, score) => `ምርጥ: ${score}%`],
      [/^Previous Best: (\d+)%$/, (_, score) => `ቀዳሚ ምርጥ: ${score}%`],
      [/^(\d+) Points$/, (_, points) => `${points} ነጥቦች`],
      [/^(\d+) Pending$/, (_, count) => `${count} በመጠባበቅ ላይ`],
      [/^(\d+) subjects cached locally$/, (_, count) => `${count} ትምህርቶች በአካባቢው ተቀምጠዋል`],
      [/^Submit \((\d+)\/(\d+) Answered\)$/, (_, answered, total) => `ያስገቡ (${answered}/${total} ተመልሰዋል)`],
      [/^Serving offline digital edition for (.+)\.$/, (_, title) => `የ${title} ዲጂታል እትም ከመስመር ውጭ በማቅረብ ላይ።`],
      [/^Textbook '(.+)' registered successfully in the Ethiopian Digital Library!$/, (_, title) => `መጽሐፉ "${title}" በኢትዮጵያ ዲጂታል ቤተ-መጻሕፍት ውስጥ በተሳካ ሁኔታ ተመዝግቧል!`]
    ];
    for (const [pattern, formatter] of dynamicPatterns) {
      const match = value.match(pattern);
      if (match) return formatter(...match);
    }

    const backMatch = value.match(/^(←\s*)?Back to (.+)$/);
    if (backMatch) return `${backMatch[1] || ''}ወደ ${backMatch[2]} ተመለስ`;

    if (value.endsWith(' - Offline LMS')) {
      return `${value.slice(0, -' - Offline LMS'.length)} - ${translations['Offline LMS']}`;
    }
    return null;
  }

  function localizeTextNode(node) {
    if (registeredText.has(node)) return;
    registeredText.add(node);
    if (node.parentElement && node.parentElement.closest('span[lang="am"]')) return;

    const parent = node.parentElement;
    if (parent && Array.from(parent.children).some(child => child.matches('span[lang="am"]'))) {
      if (isAmharic) {
        node.nodeValue = '';
      } else {
        node.nodeValue = node.nodeValue.replace(/\s*\/\s*$/, ' ');
      }
      return;
    }
    const original = node.nodeValue;
    const trimmed = original.trim();
    if (!trimmed) return;
    if (!isAmharic) {
      const englishOnly = stripAmharicSuffix(trimmed);
      if (englishOnly !== trimmed) node.nodeValue = original.replace(trimmed, englishOnly);
      return;
    }

    const translated = getTranslation(trimmed);
    if (translated) {
      const start = original.indexOf(trimmed);
      node.nodeValue = original.slice(0, start) + translated + original.slice(start + trimmed.length);
    } else {
      const gradeMatch = trimmed.match(/^Grade (\d+)$/);
      if (gradeMatch) node.nodeValue = original.replace(trimmed, `${gradeMatch[1]}ኛ ክፍል`);
    }
  }

  function localizeElement(element) {
    element.querySelectorAll('span[lang="am"]').forEach(span => {
      span.style.display = isAmharic ? '' : 'none';
    });

    const attributeTargets = [element, ...element.querySelectorAll('[placeholder], [title], [aria-label], [alt]')];
    attributeTargets.forEach(target => {
      ['placeholder', 'title', 'aria-label', 'alt'].forEach(attribute => {
        const value = target.getAttribute(attribute);
        if (!value) return;
        if (isAmharic && translations[value]) {
          target.setAttribute(attribute, translations[value]);
        } else if (!isAmharic) {
          target.setAttribute(attribute, stripAmharicSuffix(value));
        }
      });
    });

    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        return node.parentElement && node.parentElement.closest('script, style')
          ? NodeFilter.FILTER_REJECT
          : NodeFilter.FILTER_ACCEPT;
      }
    });
    let node;
    while ((node = walker.nextNode())) localizeTextNode(node);
  }

  localizeElement(document.documentElement);
  const observer = new MutationObserver(records => {
    records.forEach(record => {
      record.addedNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE) {
          localizeTextNode(node);
        } else if (node.nodeType === Node.ELEMENT_NODE) {
          localizeElement(node);
        }
      });
    });
  });
  observer.observe(document.body, { childList: true, subtree: true });
})();
