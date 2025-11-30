"use client"

import { useState } from "react"
import DetectionDashboard from "@/components/detection-dashboard"
import UploadSection from "@/components/upload-section"
import ResultsPanel from "@/components/results-panel"
import AlertCenter from "@/components/alert-center"
import SiteHeader from "@/components/site-header"
import TickerAlert from "@/components/ticker-alert"

interface Detection {
  id: number
  image: string
  timestamp: string
  detections: any[]
  vehicleSpeed: number
  riskLevel: "critical" | "warning" | "caution" | "safe"
  crossingProbability: number
  distanceToRoad: number
}

export default function Home() {
  const [detections, setDetections] = useState<Detection[]>([])
  const [selectedDetection, setSelectedDetection] = useState<Detection | null>(null)
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
    <main className="min-h-screen bg-background font-sans antialiased">
      <TickerAlert detection={selectedDetection} />
      <SiteHeader />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white pb-16 pt-24 dark:from-slate-950 dark:to-background">
        <div className="container relative z-10 mx-auto max-w-7xl px-4 text-center">
          <div className="mx-auto max-w-3xl space-y-6">
            <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-5xl md:text-6xl">
              AI-Powered <span className="text-blue-600">Wildlife Protection</span>
            </h1>
            <p className="mx-auto max-w-2xl text-lg text-slate-600 dark:text-slate-400">
              Real-time detection and risk assessment system to prevent wildlife-vehicle collisions. 
              Upload an image to analyze potential crossing risks instantly.
            </p>
          </div>

          <div className="mt-12">
            <div className="mx-auto max-w-2xl rounded-2xl bg-white p-2 shadow-xl ring-1 ring-slate-200/50 dark:bg-slate-900 dark:ring-slate-800">
              <UploadSection onUpload={handleImageUpload} isLoading={isLoading} />
            </div>
          </div>
        </div>
        
        {/* Decorative background elements */}
        <div className="absolute left-1/2 top-0 -z-10 -translate-x-1/2 blur-3xl xl:-top-6">
          <div className="aspect-[1155/678] w-[72.1875rem] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-20" 
               style={{ clipPath: 'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)' }} 
          />
        </div>
      </section>

      {/* Dashboard Section - Only visible when there is data or a selection */}
      {(selectedDetection || detections.length > 0) && (
        <section className="border-t border-slate-200 bg-slate-50 py-12 dark:border-slate-800 dark:bg-slate-950/50">
          <div className="container mx-auto max-w-7xl px-4">
            <div className="mb-8 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Analysis Dashboard</h2>
              <div className="rounded-full bg-blue-100 px-4 py-1 text-sm font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                {detections.length} Active Monitors
              </div>
            </div>

            <div className="grid gap-8 lg:grid-cols-3">
              {/* Main Visualization */}
              <div className="lg:col-span-2 space-y-6">
                {selectedDetection ? (
                  <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
                    <div className="border-b border-slate-200 px-6 py-4 dark:border-slate-800">
                      <h3 className="font-semibold text-slate-900 dark:text-white">Live Detection Feed</h3>
                    </div>
                    <div className="p-6">
                      <DetectionDashboard detection={selectedDetection} />
                    </div>
                  </div>
                ) : (
                  <div className="flex h-64 items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50 dark:border-slate-700 dark:bg-slate-900/50">
                    <p className="text-slate-500">Select a detection to view details</p>
                  </div>
                )}
              </div>

              {/* Sidebar Info */}
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
        </section>
      )}
    </main>
  )
}
