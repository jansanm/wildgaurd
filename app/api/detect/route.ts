import { type NextRequest, NextResponse } from "next/server"
import { writeFile, unlink } from "fs/promises"
import { join } from "path"
import { tmpdir } from "os"
import { spawn } from "child_process"
import path from "path"

// This uses the local YOLO Python script for accurate wildlife detection
export async function POST(request: NextRequest) {
  let tempFilePath = ""
  try {
    const formData = await request.formData()
    const file = formData.get("file") as File

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    // Save file temporarily
    const buffer = Buffer.from(await file.arrayBuffer())
    const tempDir = tmpdir()
    const fileName = `upload-${Date.now()}-${Math.random().toString(36).substring(7)}.jpg`
    tempFilePath = join(tempDir, fileName)
    
    await writeFile(tempFilePath, buffer)

    // Run Python detection script
    const projectRoot = process.cwd()
    const pythonScript = join(projectRoot, "detect_cli.py")
    const pythonPath = join(projectRoot, "venv", "bin", "python")

    const detectionResult = await runPythonScript(pythonPath, pythonScript, tempFilePath)

    return NextResponse.json(detectionResult)

  } catch (error) {
    console.error("Detection error:", error)
    return NextResponse.json({ error: "Detection failed: " + (error as Error).message }, { status: 500 })
  } finally {
    // Cleanup temp file
    if (tempFilePath) {
      try {
        await unlink(tempFilePath)
      } catch (e) {
        console.error("Failed to delete temp file:", e)
      }
    }
  }
}

function runPythonScript(pythonPath: string, scriptPath: string, imagePath: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const process = spawn(pythonPath, [scriptPath, imagePath])
    
    let stdoutData = ""
    let stderrData = ""

    process.stdout.on("data", (data) => {
      stdoutData += data.toString()
    })

    process.stderr.on("data", (data) => {
      stderrData += data.toString()
    })

    process.on("close", (code) => {
      if (code !== 0) {
        console.error("Python script error:", stderrData)
        reject(new Error(`Python script exited with code ${code}: ${stderrData}`))
        return
      }

      try {
        const result = JSON.parse(stdoutData)
        if (result.error) {
          reject(new Error(result.error))
        } else {
          resolve(result)
        }
      } catch (e) {
        console.error("Failed to parse Python output:", stdoutData)
        reject(new Error("Failed to parse detection results"))
      }
    })
  })
}
