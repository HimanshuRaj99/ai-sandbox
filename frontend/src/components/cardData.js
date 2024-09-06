export const cards = [
    {
        id: 1,
        title: 'Character Chatbot',
        description: 'Talk to your favorite character.',
        icon: '<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g clip-path="url(#clip0_901_3019)"> <path d="M24 31H8H1C1 31 1.69 27.38 2 26C2.21 25.08 3 23 11 22C11 22 12 25 16 25C20 25 21 22 21 22C29 23 29.79 25.02 30 26C30.29 27.38 31 31 31 31H24Z" fill="#FFC44D"></path> <path d="M23 8H22H10H9C9 4.13 12.13 1 16 1C19.87 1 23 4.13 23 8Z" fill="#668077"></path> <path d="M22 8V11C22 14.87 19 18 16 18C13 18 10 14.87 10 11V8H22Z" fill="#FFE6EA"></path> <path d="M1 31C1 31 1.687 27.379 2 26C2.208 25.083 3 23 11 22C11 22 12 25 16 25C20 25 21 22 21 22C29 23 29.792 25.021 30 26C30.294 27.384 31 31 31 31M10 11C10 14.866 13 18 16 18C19 18 22 14.866 22 11M8 30V31M24 30V31M6 8H23C23 4.134 19.866 1 16 1C12.134 1 9 4.134 9 8" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g> <defs> <clipPath id="clip0_901_3019"> <rect width="32" height="32" fill="white"></rect> </clipPath> </defs> </g></svg>',
        isNew: false,
        route: '/character-chatbot',
        isActivity: false,
        isTool: true
    },
    {
        id: 2,
        title: "Search to Reveal",
        description: "Get meaning and morphology of word.",
        icon: "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='40' cy='40' r='25' stroke='#FFB700' stroke-width='8' fill='none'/><line x1='60' y1='60' x2='85' y2='85' stroke='#FFB700' stroke-width='8' stroke-linecap='round'/><line x1='30' y1='40' x2='50' y2='40' stroke='#FFB700' stroke-width='4' stroke-linecap='round'/><line x1='40' y1='30' x2='40' y2='50' stroke='#FFB700' stroke-width='4' stroke-linecap='round'/></svg>",
        isNew: false,
        route: "/search-to-reveal",
        isActivity: true,
        isTool: false,
        tags: ["Morphology"]
    },
    {
        id: 3,
        title: 'Word Play',
        description: 'Tap and build words by matching prefix, root, and suffix.',
        icon: '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="6" width="6" height="6" rx="1" fill="#4CAF50"/><rect x="9" y="6" width="6" height="6" rx="1" fill="#2196F3"/><rect x="16" y="6" width="6" height="6" rx="1" fill="#FFC107"/><rect x="5" y="14" width="6" height="6" rx="1" fill="#9C27B0"/><rect x="13" y="14" width="6" height="6" rx="1" fill="#FF5722"/><path d="M4 8.5H6" stroke="white" stroke-width="1.5" stroke-linecap="round"/><path d="M11 8.5H13" stroke="white" stroke-width="1.5" stroke-linecap="round"/><path d="M18 8.5H20" stroke="white" stroke-width="1.5" stroke-linecap="round"/><path d="M7 16.5H9" stroke="white" stroke-width="1.5" stroke-linecap="round"/><path d="M15 16.5H17" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>',
        isNew: false,
        route: '/wordplay',
        isActivity: true,
        isTool: false,
        tags: ['Morphology']
    },
    {
        id: 4,
        title: "Synonym Swap",
        description: "Enhance vocabulary with synonym swaps.",
        icon: "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M20 30 L70 30 L60 20 M70 30 L60 40' stroke='#FF4500' stroke-width='10' stroke-linecap='round' stroke-linejoin='round' fill='none'/><path d='M80 70 L30 70 L40 60 M30 70 L40 80' stroke='#1E90FF' stroke-width='10' stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>",
        isNew: true,
        route: "/synonym-swap",
        isActivity: true,
        isTool: false,
        tags: ["Morphology"]
    }
];
