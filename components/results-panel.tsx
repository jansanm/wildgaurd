"use client"

interface ResultsPanelProps {
  detections: any[]
  selectedDetection: any
  onSelect: (detection: any) => void
}

export default function ResultsPanel({ detections, selectedDetection, onSelect }: ResultsPanelProps) {
  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <h3 className="mb-4 font-semibold text-foreground">Recent Detections</h3>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {detections.length === 0 ? (
          <p className="text-sm text-muted-foreground">No detections yet</p>
        ) : (
          detections.map((det) => (
            <button
              key={det.id}
              onClick={() => onSelect(det)}
              className={`w-full rounded-lg border-2 p-3 text-left transition-colors ${
                selectedDetection?.id === det.id
                  ? "border-primary bg-primary/5"
                  : "border-border hover:border-primary/50"
              }`}
            >
              <p className="text-sm font-medium text-foreground">{det.timestamp}</p>
              <p className="text-xs text-muted-foreground">{det.detections.length} animals</p>
              <div className="mt-2 flex gap-1">
                {det.detections.map((d: any) => (
                  <span key={d.id} className="inline-block rounded bg-primary/10 px-2 py-1 text-xs text-primary">
                    {d.animal}
                  </span>
                ))}
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}
