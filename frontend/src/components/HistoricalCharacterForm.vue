<template>
  <div class="historical-character-form">
    <div class="form-container">
      <div class="form-header">
        <h1 class="heading">Character Chatbot</h1>
      </div>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="gradeLevel">Grade level</label>
          <select id="gradeLevel" v-model="formData.gradeLevel" required>
            <option disabled value="">Select Grade level</option>
            <option v-for="option in gradeLevelOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="version">Variant</label>
          <div class="select-with-info">
            <select id="version" v-model="formData.version" required>
              <option disabled value="">Select Variant</option>
              <option v-for="option in versionOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
            <div class="tooltip">
              <p><strong>Variant 1:</strong> {{ variantInfo['Version 1'] }}</p>
              <p><strong>Variant 2:</strong> {{ variantInfo['Version 2'] }}</p>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label for="standard">Educational Standards</label>
          <div class="select-with-info">
            <select id="standard" v-model="formData.standard">
              <option disabled value="">Select Educational Standards</option>
              <option v-for="option in standardOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="provider">Provider</label>
          <select id="provider" v-model="formData.provider" required @change="resetModel">
            <option disabled value="">Select Provider</option>
            <option v-for="provider in providerOptions" :key="provider" :value="provider">
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="model">Model</label>
          <select id="model" v-model="formData.model" required :disabled="!formData.provider">
            <option disabled value="">Select Model</option>
            <option v-for="model in availableModels" :key="model.id" :value="model.id">
              {{ model.id }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="instructions">Type your Character details</label>
          <textarea id="instructions" v-model="formData.instructions"
            placeholder="E.g. Paul Revere from American Revolution..." rows="3" required></textarea>
        </div>
        <button type="submit" class="submit-btn" :disabled="isLoading">Submit</button>
      </form>
    </div>
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script>
import { API_ENDPOINTS, BASE_URL } from '@/constants';
import modelListData from '@/assets/model_list.json';

export default {
  name: 'ConfigureComponent',
  props: {
    initialFormData: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      formData: {
        gradeLevel: this.initialFormData?.gradeLevel || '',
        instructions: this.initialFormData?.instructions || '',
        provider: this.initialFormData?.provider || '',
        model: this.initialFormData?.model || '',
        version: this.initialFormData?.version || '',
        standard: this.initialFormData?.standard || ''
      },
      gradeLevelOptions: [
        { value: 3, label: 'Grade 3' },
        { value: 4, label: 'Grade 4' },
        { value: 5, label: 'Grade 5' }
      ],
      versionOptions: [
        { value: 'Version 1', label: 'Variant 1' },
        { value: 'Version 2', label: 'Variant 2' }
      ],
      standardOptions: [
        { value: 'common_core', label: 'Common Core' },
        { value: 'ngss', label: 'NGSS' },
        { value: 'state_board', label: 'State Standards' },
        { value: 'international', label: 'International Standards' }
      ],
      variantInfo: {
        'Version 1': 'Provides responses based on the characters provided by the user with a fixed prompt.',
        'Version 2': 'Generates dynamic prompts based on the characters provided by the user and provides detailed responses.'
      },
      models: [],
      isLoading: false
    };
  },
  computed: {
    providerOptions() {
      return [...new Set(this.models.map(model => model.owned_by))];
    },
    availableModels() {
      return this.models.filter(model => model.owned_by === this.formData.provider);
    },
  },
  mounted() {
    this.initializeOptions();
    this.fetchModels();
  },
  methods: {
    initializeOptions() {
      this.addOptionIfNotExists(this.gradeLevelOptions, this.formData.gradeLevel, (value) => ({ value, label: `Grade ${value}` }));
      this.addOptionIfNotExists(this.versionOptions, this.formData.version);
      this.addOptionIfNotExists(this.standardOptions, this.formData.standard);
    },
    addOptionIfNotExists(options, value, transform = (value) => ({ value, label: value })) {
      if (value && !options.some(option => option.value === value)) {
        options.push(transform(value));
      }
    },
    async fetchModels() {
      // try {
      //   const response = await fetch(`${BASE_URL}${API_ENDPOINTS.MODELS}`);
      //   const data = await response.json();
      //   this.models = data.data;
      // } catch (error) {
      //   console.error('Error fetching models:', error);
      // }
      this.models = modelListData.data;
    },
    resetModel() {
      this.formData.model = '';
    },
    async handleSubmit() {
      this.isLoading = true;
      const payload = {
        provider: this.formData.provider,
        model: this.formData.model,
        character: this.formData.instructions,
        grade: parseInt(this.formData.gradeLevel),
        version: this.formData.version,
        standard: this.formData.standard
      };

      try {
        console.log('Submitting configure request with payload:', JSON.stringify(payload, null, 2));

        const configureResponse = await fetch(`${BASE_URL}${API_ENDPOINTS.CONFIGURE}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload)
        });

        if (!configureResponse.ok) {
          throw new Error(`Configure HTTP error! status: ${configureResponse.status}`);
        }

        console.log('Configure request successful. Sending chat request...');

        const chatResponse = await fetch(`${BASE_URL}${API_ENDPOINTS.CHAT}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: 'Hello, who are you?' })
        });

        if (!chatResponse.ok) {
          throw new Error(`Chat HTTP error! status: ${chatResponse.status}`);
        }

        const chatResult = await chatResponse.json();
        console.log('Chat result:', chatResult);

        // Navigate to the chat component
        this.$router.push({
          path: '/chatbot',
          query: {
            gradeLevel: this.formData.gradeLevel,
            instructions: encodeURIComponent(this.formData.instructions),
            provider: this.formData.provider,
            model: this.formData.model,
            version: this.formData.version,
            standard: this.formData.standard,
            initialMessage: encodeURIComponent(JSON.stringify(chatResult))
          }
        });

      } catch (error) {
        console.error('Error in handleSubmit:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.historical-character-form {
  font-family: 'Inter', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  max-height: 100vh;
  padding: 20px;
  background-color: #f5f5f5;
}

.form-container {
  width: 100%;
  max-width: 500px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 0px 20px 20px 20px;
}

.form-header {
  margin-bottom: 20px;
}

.site-title {
  text-align: center;
  font-size: 18px;
  color: #888;
  margin: 0 0 5px 0;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

select,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

textarea {
  resize: vertical;
}

.select-with-info {
  position: relative;
}

.tooltip {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  z-index: 1;
  width: 60%;
  top: 100%;
  left: 0;
  margin-top: 5px;
  font-size: 12px;
}

.select-with-info:hover .tooltip {
  display: block;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.submit-button:hover {
  background-color: #333;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #333;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 600px) {
  .form-container {
    padding: 15px;
  }

  .site-title {
    font-size: 16px;
  }

  select,
  textarea,
  .submit-button {
    font-size: 14px;
  }
}
</style>