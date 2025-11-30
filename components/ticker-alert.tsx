"use client"

import { useEffect, useState } from "react"
import { AlertTriangle } from "lucide-react"

interface TickerAlertProps {
  detection: any
}

export default function TickerAlert({ detection }: TickerAlertProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    if (detection && (detection.riskLevel === "critical" || detection.crossingProbability > 50)) {
      setIsVisible(true)
    } else {
      setIsVisible(false)
    }
  }, [detection])

  if (!isVisible) return null

  return (
    <div className="w-full bg-red-600 text-white overflow-hidden py-2 shadow-md z-50 relative">
      <div className="animate-marquee whitespace-nowrap flex items-center">
        <span className="mx-4 flex items-center text-lg font-bold uppercase tracking-wider">
          <AlertTriangle className="mr-2 h-5 w-5 fill-white text-red-600" />
          CAUTION: Wildlife Crossing Detected - Reduce Speed Immediately
        </span>
        <span className="mx-4 flex items-center text-lg font-bold uppercase tracking-wider">
          <AlertTriangle className="mr-2 h-5 w-5 fill-white text-red-600" />
          CAUTION: Wildlife Crossing Detected - Reduce Speed Immediately
        </span>
        <span className="mx-4 flex items-center text-lg font-bold uppercase tracking-wider">
          <AlertTriangle className="mr-2 h-5 w-5 fill-white text-red-600" />
          CAUTION: Wildlife Crossing Detected - Reduce Speed Immediately
        </span>
        <span className="mx-4 flex items-center text-lg font-bold uppercase tracking-wider">
          <AlertTriangle className="mr-2 h-5 w-5 fill-white text-red-600" />
          CAUTION: Wildlife Crossing Detected - Reduce Speed Immediately
        </span>
      </div>
    </div>
  )
}
