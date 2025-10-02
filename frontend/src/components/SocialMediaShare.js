import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { prepareSocialPost } from '../services/api';
import toast from 'react-hot-toast';

const platforms = [
  { id: 'instagram', name: 'Instagram', icon: '', color: 'bg-gradient-to-r from-purple-500 to-pink-500' },
  { id: 'twitter', name: 'X', icon: '', color: 'bg-blue-500' },
  { id: 'facebook', name: 'Facebook', icon: '', color: 'bg-blue-600' },
  { id: 'linkedin', name: 'LinkedIn', icon: '', color: 'bg-blue-700' }
];

const SocialMediaShare = ({ caption, image, tone }) => {
  const [selectedPlatform, setSelectedPlatform] = useState('instagram');
  const [socialData, setSocialData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePreparePost = async (platform) => {
    setSelectedPlatform(platform);
    setIsLoading(true);

    try {
      const response = await prepareSocialPost(image, platform, tone);
      setSocialData(response);
      toast.success(`Post prepared for ${platform}!`);
    } catch (error) {
      toast.error('Failed to prepare social post');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Share on Social Media</h2>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {platforms.map((platform) => (
          <motion.button
            key={platform.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handlePreparePost(platform.id)}
            className={`p-4 rounded-lg text-white font-medium transition-all ${
              selectedPlatform === platform.id ? 'ring-2 ring-offset-2 ring-purple-500' : ''
            } ${platform.color}`}
            disabled={isLoading}
          >
            <span className="text-xl">{platform.icon}</span>
            <p className="text-xs mt-1">{platform.name}</p>
          </motion.button>
        ))}
      </div>

      {socialData && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Formatted Post</h3>
            <p className="text-sm text-gray-600 whitespace-pre-wrap">{socialData.full_text}</p>
          </div>

          {socialData.hashtags && socialData.hashtags.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Suggested Hashtags</h3>
              <div className="flex flex-wrap gap-2">
                {socialData.hashtags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center justify-between text-sm text-gray-500">
            <span>Character count: {socialData.char_count}</span>
            {socialData.char_limit && (
              <span>Limit: {socialData.char_limit}</span>
            )}
          </div>

          <button
            className="w-full px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-medium rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all"
            onClick={() => {
              // Future integration with social media APIs
              toast.success('Social media integration coming soon!');
            }}
          >
            Post to {platforms.find(p => p.id === selectedPlatform)?.name}
          </button>
        </motion.div>
      )}
    </div>
  );
};

export default SocialMediaShare;