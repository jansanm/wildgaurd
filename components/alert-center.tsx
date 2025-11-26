"use client"

import { AlertTriangle, Bell, MapPin, Zap } from "lucide-react"

interface AlertCenterProps {
  detection: any
}

export default function AlertCenter({ detection }: AlertCenterProps) {
  if (!detection) {
    return (
      <div className="rounded-lg border border-border bg-card p-6">
        <div className="text-center">
          <Bell className="mx-auto mb-2 h-8 w-8 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">No detections yet</p>
        </div>
      </div>
    )
  }

  const alerts = []

  if (detection.riskLevel === "critical") {
    alerts.push({
      title: "Critical Risk Detected",
      description: "High-speed approach with high crossing probability",
      icon: AlertTriangle,
      color: "text-red-600",
      bgColor: "bg-red-50",
    })
  }

  if (detection.crossingProbability > 70) {
    alerts.push({
      title: "High Crossing Probability",
      description: `${detection.crossingProbability}% chance of road crossing`,
      icon: MapPin,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
    })
  }

  if (detection.vehicleSpeed > 80) {
    alerts.push({
      title: "High Vehicle Speed",
      description: `Traveling at ${detection.vehicleSpeed} km/h - reduce speed`,
      icon: Zap,
      color: "text-yellow-600",
      bgColor: "bg-yellow-50",
    })
  }

  if (detection.distanceToRoad < 50) {
    alerts.push({
      title: "Close to Road",
      description: `Animal is only ${detection.distanceToRoad}m from road`,
      icon: AlertTriangle,
      color: "text-red-600",
      bgColor: "bg-red-50",
    })
  }

  return (
    <div className="space-y-3">
      <h3 className="font-semibold text-foreground">Active Alerts</h3>
      {alerts.length === 0 ? (
        <div className="rounded-lg border border-border bg-green-50 p-4">
          <p className="text-sm text-green-900">✓ No critical alerts</p>
        </div>
      ) : (
        alerts.map((alert, idx) => {
          const Icon = alert.icon
          return (
            <div key={idx} className={`rounded-lg border border-current p-3 ${alert.bgColor}`}>
              <div className="flex gap-3">
                <Icon className={`h-5 w-5 flex-shrink-0 ${alert.color}`} />
                <div>
                  <p className={`text-sm font-medium ${alert.color}`}>{alert.title}</p>
                  <p className={`text-xs ${alert.color} opacity-75`}>{alert.description}</p>
                </div>
              </div>
            </div>
          )
        })
      )}
    </div>
  )
}
