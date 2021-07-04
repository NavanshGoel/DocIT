import React from 'react'
import { useCanvas } from './CanvasContext'

export const ClearCanvasButton = () => {
  const { clearCanvas } = useCanvas()

  return (
    <div>
      <button onClick={clearCanvas}>Clear Board</button>
    </div>
  )
}