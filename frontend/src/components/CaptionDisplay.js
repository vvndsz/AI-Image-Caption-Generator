import React, { useState } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const CaptionDisplay = ({ caption, captionData }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(caption);
    setCopied(true);
    toast.success('Caption copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Generated Caption</h2>
        <button
          onClick={handleCopy}
          className={`px-3 py-1 text-sm font-medium rounded-md transition-all ${
            copied
              ? 'bg-green-100 text-green-700'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          {copied ? '✓ Copied' : 'Copy'}
        </button>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="space-y-4"
      >
        <div className="p-4 bg-purple-50 rounded-lg">
          <p className="text-gray-800 leading-relaxed">{caption}</p>
        </div>

        {captionData && (
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <span className="text-gray-500">Confidence:</span>
              <div className="flex-1 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-purple-600 h-2 rounded-full"
                  style={{ width: `${captionData.confidence * 100}%` }}
                />
              </div>
              <span className="text-gray-700 font-medium">
                {(captionData.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-gray-500">Processing Time:</span>
              <span className="text-gray-700 font-medium">
                {captionData.processing_time.toFixed(2)}s
              </span>
            </div>
          </div>
        )}

        <div className="pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            Character count: {caption.length}
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default CaptionDisplay;