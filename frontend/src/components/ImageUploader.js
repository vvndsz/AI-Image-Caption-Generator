import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';

const ImageUploader = ({ onImageUpload, selectedImage }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onImageUpload(acceptedFiles[0]);
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    maxFiles: 1,
    maxSize: 10485760 // 10MB
  });

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Image</h2>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-purple-500 bg-purple-50'
            : 'border-gray-300 hover:border-purple-400'
        }`}
      >
        <input {...getInputProps()} />
        
        {selectedImage ? (
          <div className="space-y-4">
            <img
              src={URL.createObjectURL(selectedImage)}
              alt="Preview"
              className="mx-auto max-h-64 rounded-lg shadow-md"
            />
            <p className="text-sm text-gray-600">
              {selectedImage.name} ({(selectedImage.size / 1024 / 1024).toFixed(2)} MB)
            </p>
            <p className="text-sm text-purple-600">Click or drag to replace</p>
          </div>
        ) : (
          <div className="space-y-4">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            {isDragActive ? (
              <p className="text-purple-600">Drop the image here...</p>
            ) : (
              <>
                <p className="text-gray-600">
                  Drag and drop an image here, or click to select
                </p>
                <p className="text-sm text-gray-500">
                  Supports: JPEG, PNG, GIF, BMP, WebP (Max 10MB)
                </p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;