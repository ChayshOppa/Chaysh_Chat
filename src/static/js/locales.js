// Initialize translations object
let translations = {
    en: {},
    pl: {}
};

// Load translations from JSON files
async function loadTranslations() {
    try {
        const [enResponse, plResponse] = await Promise.all([
            fetch('/static/locales/en.json'),
            fetch('/static/locales/pl.json')
        ]);

        if (!enResponse.ok || !plResponse.ok) {
            throw new Error('Failed to load translations');
        }

        translations.en = await enResponse.json();
        translations.pl = await plResponse.json();

        // Initialize with saved language or default to English
        const savedLang = localStorage.getItem('language') || 'en';
        document.documentElement.setAttribute('data-lang', savedLang);
        updateTranslations();
    } catch (error) {
        console.error('Error loading translations:', error);
        // Fallback to hardcoded translations if loading fails
        translations = {
            en: {
                title: "Chaysh Assistant",
                subtitle: "AI-powered search assistant",
                searchPlaceholder: "Type your message...",
                themeToggle: "Toggle Theme",
                languageToggle: "Change Language",
                terms: "Terms & Conditions",
                error: "An error occurred while processing your request.",
                loading: "Loading...",
                askMore: "Ask More",
                tryAgain: "Try again",
                pleaseEnter: "Please enter a message",
                categories: "Available Categories",
                welcome: "Welcome to Chaysh Assistant",
                capabilities: "I can help you with:",
                tryAsking: "Try asking me something like:",
                autoDetect: "Auto-detect"
            },
            pl: {
                title: "Asystent Chaysh",
                subtitle: "Asystent wyszukiwania AI",
                searchPlaceholder: "Napisz wiadomość...",
                themeToggle: "Przełącz motyw",
                languageToggle: "Zmień język",
                terms: "Regulamin",
                error: "Wystąpił błąd podczas przetwarzania żądania.",
                loading: "Ładowanie...",
                askMore: "Zapytaj więcej",
                tryAgain: "Spróbuj ponownie",
                pleaseEnter: "Wprowadź wiadomość",
                categories: "Dostępne kategorie",
                welcome: "Witaj w Asystencie Chaysh",
                capabilities: "Mogę pomóc Ci z:",
                tryAsking: "Spróbuj zapytać mnie o:",
                autoDetect: "Auto-wykryj"
            }
        };
    }
}

// Update UI elements with translations
function updateTranslations() {
    const lang = document.documentElement.getAttribute('data-lang') || 'en';
    const currentTranslations = translations[lang] || translations.en;

    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (currentTranslations[key]) {
            element.textContent = currentTranslations[key];
        }
    });

    // Update category badges if they exist
    document.querySelectorAll('.category-badge').forEach(badge => {
        const category = badge.getAttribute('data-category');
        if (category && currentTranslations.categories && currentTranslations.categories[category]) {
            badge.textContent = currentTranslations.categories[category];
        }
    });
}

// Change language
function changeLanguage(lang) {
    localStorage.setItem('language', lang);
    document.documentElement.setAttribute('data-lang', lang);
    updateTranslations();
}

// Initialize translations when the page loads
document.addEventListener('DOMContentLoaded', loadTranslations); 