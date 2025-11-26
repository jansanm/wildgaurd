"use client"

import { AlertTriangle, AlertCircle, CheckCircle2, Clock } from "lucide-react"

interface Detection {
  id: number
  image: string
  timestamp: string
  detections: Array<{
    id: number
    animal: string
    confidence: number
    bbox: { x: number; y: number; width: number; height: number }
  }>
  vehicleSpeed: number
  riskLevel: "critical" | "warning" | "caution" | "safe"
  crossingProbability: number
  distanceToRoad: number
}

interface DetectionDashboardProps {
  detection: Detection
}

const getRiskColor = (riskLevel: string) => {
  switch (riskLevel) {
    case "critical":
      return "bg-red-50 border-red-200"
    case "warning":
      return "bg-orange-50 border-orange-200"
    case "caution":
      return "bg-yellow-50 border-yellow-200"
    case "safe":
      return "bg-green-50 border-green-200"
    default:
      return "bg-card border-border"
  }
}

const getRiskTextColor = (riskLevel: string) => {
  switch (riskLevel) {
    case "critical":
      return "text-red-900"
    case "warning":
      return "text-orange-900"
    case "caution":
      return "text-yellow-900"
    case "safe":
      return "text-green-900"
    default:
      return "text-foreground"
  }
}

const getRiskIcon = (riskLevel: string) => {
  switch (riskLevel) {
    case "critical":
      return AlertTriangle
    case "warning":
      return AlertCircle
    case "caution":
      return Clock
    case "safe":
      return CheckCircle2
    default:
      return AlertCircle
  }
}

export default function DetectionDashboard({ detection }: DetectionDashboardProps) {
  const RiskIcon = getRiskIcon(detection.riskLevel)

  return (
    <div className="space-y-6">
      {/* Image with Detections */}
      <div className="relative overflow-hidden rounded-lg border border-border bg-card">
        <div className="relative aspect-video w-full bg-muted">
          <img
            src={detection.image || "/placeholder.svg"}
            alt="Detected wildlife"
            className="h-full w-full object-cover"
          />
          {/* Bounding Boxes */}
          {detection.detections.map((det) => (
            <div
              key={det.id}
              className="absolute border-2 border-orange-400"
              style={{
                left: `${det.bbox.x}px`,
                top: `${det.bbox.y}px`,
                width: `${det.bbox.width}px`,
                height: `${det.bbox.height}px`,
              }}
            >
              <div className="bg-orange-400 px-2 py-1 text-xs font-bold text-white">
                {det.animal} {(det.confidence * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Assessment Card */}
      <div className={`rounded-lg border-2 p-6 ${getRiskColor(detection.riskLevel)}`}>
        <div className="flex items-start gap-4">
          <RiskIcon className={`h-6 w-6 flex-shrink-0 ${getRiskTextColor(detection.riskLevel)}`} />
          <div className="flex-1">
            <h3 className={`text-lg font-bold ${getRiskTextColor(detection.riskLevel)}`}>
              Risk Level: {detection.riskLevel.toUpperCase()}
            </h3>
            <p className={`mt-1 text-sm ${getRiskTextColor(detection.riskLevel)}`}>Detected at {detection.timestamp}</p>
          </div>
        </div>
      </div>

      {/* Detections Grid */}
      <div className="grid gap-4 sm:grid-cols-2">
        {detection.detections.map((det) => (
          <div key={det.id} className="rounded-lg border border-border bg-card p-4">
            <div className="flex items-start justify-between">
              <div>
                <p className="font-semibold text-foreground">{det.animal}</p>
                <p className="text-sm text-muted-foreground">Confidence</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-primary">{det.confidence.toFixed(1)}%</p>
                <div className="mt-1 h-2 w-24 overflow-hidden rounded-full bg-muted">
                  <div className="h-full bg-primary" style={{ width: `${det.confidence}%` }} />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Metrics */}
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-xs font-medium uppercase text-muted-foreground">Vehicle Speed</p>
          <p className="mt-2 text-3xl font-bold text-primary">{detection.vehicleSpeed} km/h</p>
        </div>
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-xs font-medium uppercase text-muted-foreground">Crossing Probability</p>
          <p className="mt-2 text-3xl font-bold text-orange-600">{detection.crossingProbability}%</p>
        </div>
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-xs font-medium uppercase text-muted-foreground">Distance to Road</p>
          <p className="mt-2 text-3xl font-bold text-green-600">{detection.distanceToRoad}m</p>
        </div>
      </div>
    </div>
  )
}
