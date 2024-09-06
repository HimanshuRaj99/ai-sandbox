import { createRouter, createWebHistory } from 'vue-router';
import AllToolActivityView from '../views/AllToolActivityView.vue';
import ActivityView from '@/views/ActivityView.vue';
import ToolsView from '@/views/ToolsView.vue';
import HistoricalCharacterView from '@/views/HistoricalCharacterView.vue';
import ChatbotView from '@/views/ChatbotView.vue';
import EditPromptView from '@/views/EditPromptView.vue';
import ClickToRevealView from '@/views/ClickToRevealView.vue';
import FeedbackView from '@/views/FeedbackView.vue';
import LoginView from '../views/LoginView.vue';
// import DocumentUploadComponent from '@/views/DocumentUploadComponent.vue';
import LessonActivities from '../components/LessonActivities.vue';
import WordplayGame from '../components/WordplayGame.vue';
import SynonymSwapInput from '../views/SynonymSwapInput.vue';
import SynonymSwapActivity from '../views/SynonymSwapActivity.vue';
import ConfigGrammar from '../components/ConfigGrammar.vue';
import IdentifyGrammarElement from '../views/IdentifyGrammarElement.vue';
import SequenceStoryInput from '../views/SequenceStoryInput.vue';
import SequenceStoryView from '../views/SequenceStoryView.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/home', name: 'AllToolActivityView', component: AllToolActivityView, meta: { requiresAuth: true } },
  { path: '/tools', name: 'ToolsView', component: ToolsView, meta: { requiresAuth: true } },
  // { path: '/document-upload', name: 'DocumentUpload', component: DocumentUploadComponent, meta: { requiresAuth: true } },
  { path: '/activities', name: 'ActivityView', component: ActivityView, meta: { requiresAuth: true } },
  { path: '/character-chatbot', name: 'HistoricalCharacterView', component: HistoricalCharacterView, meta: { requiresAuth: true } },
  { path: '/chatbot', name: 'ChatbotView', component: ChatbotView, meta: { requiresAuth: true } },
  { path: '/edit-prompt', name: 'EditPromptView', component: EditPromptView , meta: { requiresAuth: true } },
  { path: '/search-to-reveal', name: 'ClickToRevealView', component: ClickToRevealView , meta: { requiresAuth: true } },
  { path: '/feedback', name: 'FeedbackView', component: FeedbackView, meta: { requiresAuth: true } },
  { path: '/wordplay', name: 'LessonActivities', component: LessonActivities, meta: { requiresAuth: true } },
  { path: '/WordplayGame', name: 'WordplayGame', component: WordplayGame, meta: { requiresAuth: true } },
  { path: '/synonym-swap', name: 'SynonymSwapInput', component: SynonymSwapInput, meta: { requiresAuth: true } },
  { path: '/synonym-swap-activity/', name: 'SynonymSwapActivity', component: SynonymSwapActivity, props: true, meta: { requiresAuth: true } },
  { path: '/sub-pred', name: 'ConfigGrammar', component: ConfigGrammar, meta: { requiresAuth: true } },
  { path: '/sub-pred-activity', name: 'IdentifyGrammarElement', component: IdentifyGrammarElement, meta: { requiresAuth: true } },
  { path: '/sequence-story/', name: 'SequenceStoryInput', component: SequenceStoryInput, props: true, meta: { requiresAuth: true } },
  { path: '/sequence-story-activity', name: 'SequenceStoryView', component: SequenceStoryView, meta: { requiresAuth: true } },
  { path: '/', redirect: '/home' },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  console.log('Validating token')
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  console.log('isAuthenticated:' + isAuthenticated)
  console.log('Requires Auth:' + to.meta.requiresAuth)
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;