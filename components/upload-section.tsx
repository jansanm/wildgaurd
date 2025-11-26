"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Upload, Loader2 } from "lucide-react"

interface UploadSectionProps {
  onUpload: (file: File) => void
  isLoading: boolean
}

export default function UploadSection({ onUpload, isLoading }: UploadSectionProps) {
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      onUpload(files[0])
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0])
    }
  }

  return (
    <div
      className={`rounded-lg border-2 border-dashed transition-colors ${
        dragActive ? "border-primary bg-primary/5" : "border-border bg-card hover:border-primary/50"
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center justify-center px-6 py-12">
        {isLoading ? (
          <>
            <Loader2 className="mb-4 h-12 w-12 animate-spin text-primary" />
            <p className="text-lg font-medium text-foreground">Processing image...</p>
            <p className="text-sm text-muted-foreground">Analyzing for wildlife detection</p>
          </>
        ) : (
          <>
            <Upload className="mb-4 h-12 w-12 text-primary" />
            <p className="text-lg font-medium text-foreground">Drop image here to analyze</p>
            <p className="text-sm text-muted-foreground">or click to browse</p>
            <input ref={fileInputRef} type="file" accept="image/*" onChange={handleChange} className="hidden" />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="mt-4 rounded-lg bg-primary px-6 py-2 font-medium text-primary-foreground hover:opacity-90 transition-opacity"
            >
              Select Image
            </button>
          </>
        )}
      </div>
    </div>
  )
}
