import React from 'react';
import { RadioGroup } from '@headlessui/react';
import { CheckCircleIcon } from '@heroicons/react/24/solid';

const tones = [
  {
    value: 'formal',
    label: 'Formal',
    description: 'Professional and descriptive',
    icon: '👔'
  },
  {
    value: 'casual',
    label: 'Casual',
    description: 'Friendly and conversational',
    icon: '😊'
  },
  {
    value: 'humorous',
    label: 'Humorous',
    description: 'Witty and entertaining',
    icon: '😄'
  },
  {
    value: 'poetic',
    label: 'Poetic',
    description: 'Lyrical and evocative',
    icon: '✨'
  },
  {
    value: 'technical',
    label: 'Technical',
    description: 'Precise and detailed',
    icon: '🔬'
  },
  {
    value: 'marketing',
    label: 'Marketing',
    description: 'Engaging and persuasive',
    icon: '📢'
  },
  {
    value: 'storytelling',
    label: 'Storytelling',
    description: 'Narrative and engaging',
    icon: '📖'
  }
];

const ToneSelector = ({ selectedTone, onToneChange }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Tone</h2>
      
      <RadioGroup value={selectedTone} onChange={onToneChange}>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {tones.map((tone) => (
            <RadioGroup.Option
              key={tone.value}
              value={tone.value}
              className={({ active, checked }) =>
                `${active ? 'ring-2 ring-purple-600' : ''}
                ${checked ? 'bg-purple-50 border-purple-600' : 'bg-white'}
                relative flex cursor-pointer rounded-lg px-4 py-3 border focus:outline-none`
              }
            >
              {({ checked }) => (
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">{tone.icon}</span>
                    <div>
                      <RadioGroup.Label
                        as="p"
                        className={`font-medium ${
                          checked ? 'text-purple-900' : 'text-gray-900'
                        }`}
                      >
                        {tone.label}
                      </RadioGroup.Label>
                      <RadioGroup.Description
                        as="span"
                        className={`text-sm ${
                          checked ? 'text-purple-700' : 'text-gray-500'
                        }`}
                      >
                        {tone.description}
                      </RadioGroup.Description>
                    </div>
                  </div>
                  {checked && (
                    <CheckCircleIcon className="h-5 w-5 text-purple-600" />
                  )}
                </div>
              )}
            </RadioGroup.Option>
          ))}
        </div>
      </RadioGroup>
    </div>
  );
};

export default ToneSelector;