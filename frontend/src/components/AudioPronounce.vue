<template>
  <div class="audio-pronounce">
    <div class="meaning-header">
      <button @click="toggleAudio" class="pronounce-button" :title="buttonText">
        <svg v-if="!playing" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
          <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00cc00" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="6" y="4" width="4" height="16"></rect>
          <rect x="14" y="4" width="4" height="16"></rect>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { API_ENDPOINTS, BASE_URL } from '@/constants';

export default {
  name: 'AudioPronounce',
  props: {
    definition: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      audioPlayer: null,
      buttonText: 'Read Aloud',
      playing: false,
      audioUrl: null
    };
  },
  methods: {
    async toggleAudio() {
      if (this.playing) {
        this.pauseAudio();
      } else {
        await this.playAudio();
      }
    },
    pauseAudio() {
      if (this.audioPlayer) {
        this.audioPlayer.pause();
        this.playing = false;
        this.buttonText = 'Read Aloud';
      }
    },
    async playAudio() {
      if (!this.audioUrl) {
        await this.fetchAudio();
      }
      
      if (this.audioPlayer) {
        this.audioPlayer.play();
      } else {
        this.audioPlayer = new Audio(this.audioUrl);
        this.audioPlayer.play();
        
        this.audioPlayer.onended = () => {
          this.playing = false;
          this.buttonText = 'Read Aloud';
        };
      }
      
      this.playing = true;
      this.buttonText = 'Pause';
    },
    async fetchAudio() {
      const apiEndpoint = `${BASE_URL}${API_ENDPOINTS.CLICK_TO_PRONOUNCE}`;
      const data = { word: this.definition };
      try {
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const audioBlob = await response.blob();
        this.audioUrl = URL.createObjectURL(audioBlob);
      } catch (error) {
        console.error('Error fetching audio:', error);
      }
    }
  },
  beforeUnmount() {
    if (this.audioPlayer) {
      this.audioPlayer.pause();
      this.audioPlayer = null;
    }
    if (this.audioUrl) {
      URL.revokeObjectURL(this.audioUrl);
    }
  }
}
</script>

<style scoped>
.audio-pronounce {
  width: 100%;
}

.meaning-header {
  display: flex;
  align-items: center;
  /* margin-bottom: 10%; */
}

.pronounce-button {
  background-color: transparent;
  border: none;
  padding: 0;
  border-radius: 1px;
  cursor: pointer;
  font-size: 0.8em;
  transition: background-color 0.3s ease;
}

.pronounce-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.pronounce-button svg {
  margin-right: 5px;
}

.pronounce-button svg polyline {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: stroke-offset 0.5s ease forwards;
}

@keyframes stroke-offset {
  to {
    stroke-dashoffset: 0;
  }
}
</style>