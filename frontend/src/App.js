import React, { useState, useCallback } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';
import ImageUploader from './components/ImageUploader';
import ToneSelector from './components/ToneSelector';
import CaptionDisplay from './components/CaptionDisplay';
import SocialMediaShare from './components/SocialMediaShare';
import { generateCaption } from './services/api';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedTone, setSelectedTone] = useState('casual');
  const [caption, setCaption] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [captionData, setCaptionData] = useState(null);

  const handleImageUpload = useCallback((file) => {
    setSelectedImage(file);
    setCaption('');
    setCaptionData(null);
  }, []);

  const handleGenerateCaption = async () => {
    if (!selectedImage) {
      toast.error('Please upload an image first');
      return;
    }

    setIsLoading(true);
    try {
      const response = await generateCaption(selectedImage, selectedTone);
      setCaption(response.caption);
      setCaptionData(response);
      toast.success('Caption generated successfully!');
    } catch (error) {
      toast.error('Failed to generate caption. Please try again.');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setCaption('');
    setCaptionData(null);
    setSelectedTone('casual');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <svg className="w-8 h-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h1 className="text-2xl font-bold text-gray-900">AI Caption Generator</h1>
            </div>
            {selectedImage && (
              <button
                onClick={handleReset}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Start Over
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload & Settings */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <ImageUploader 
                onImageUpload={handleImageUpload}
                selectedImage={selectedImage}
              />
            </motion.div>

            {selectedImage && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
              >
                <ToneSelector
                  selectedTone={selectedTone}
                  onToneChange={setSelectedTone}
                />
              </motion.div>
            )}

            {selectedImage && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <button
                  onClick={handleGenerateCaption}
                  disabled={isLoading}
                  className={`w-full px-6 py-3 text-white font-medium rounded-lg shadow-lg transform transition-all ${
                    isLoading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 hover:scale-105'
                  }`}
                >
                  {isLoading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Generating Caption...
                    </span>
                  ) : (
                    'Generate Caption'
                  )}
                </button>
              </motion.div>
            )}
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            <AnimatePresence>
              {caption && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.5 }}
                >
                  <CaptionDisplay
                    caption={caption}
                    captionData={captionData}
                  />
                </motion.div>
              )}
            </AnimatePresence>

            <AnimatePresence>
              {caption && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                >
                  <SocialMediaShare
                    caption={caption}
                    image={selectedImage}
                    tone={selectedTone}
                  />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;