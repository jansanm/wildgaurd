"use client"

import { useState } from "react"
import DetectionDashboard from "@/components/detection-dashboard"
import UploadSection from "@/components/upload-section"
import ResultsPanel from "@/components/results-panel"
import AlertCenter from "@/components/alert-center"

export default function Home() {
  const [detections, setDetections] = useState([])
  const [selectedDetection, setSelectedDetection] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleImageUpload = async (file: File) => {
    setIsLoading(true)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("/api/detect", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Detection failed")
      }

      const result = await response.json()

      const newDetection = {
        id: Date.now(),
        image: URL.createObjectURL(file),
        timestamp: new Date().toLocaleTimeString(),
        detections: result.detections,
        vehicleSpeed: result.vehicleSpeed || 65,
        riskLevel: result.riskLevel,
        crossingProbability: result.crossingProbability,
        distanceToRoad: result.distanceToRoad,
      }

      setDetections([newDetection, ...detections])
      setSelectedDetection(newDetection)
    } catch (error) {
      console.error("Error during detection:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="mx-auto max-w-7xl px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-balance text-3xl font-bold text-foreground">WildGuard</h1>
              <p className="text-muted-foreground">Wildlife Detection & Risk Assessment System</p>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium text-foreground">Active Monitors</div>
              <div className="text-2xl font-bold text-primary">{detections.length}</div>
            </div>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            <UploadSection onUpload={handleImageUpload} isLoading={isLoading} />
            {selectedDetection && <DetectionDashboard detection={selectedDetection} />}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <AlertCenter detection={selectedDetection} />
            <ResultsPanel
              detections={detections}
              selectedDetection={selectedDetection}
              onSelect={setSelectedDetection}
            />
          </div>
        </div>
      </div>
    </main>
  )
}
