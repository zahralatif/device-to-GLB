import {
  Suspense,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { Html, OrbitControls, useGLTF } from '@react-three/drei'
import * as THREE from 'three'

interface ModelCard {
  id: string
  label: string
  type: string
  dimensions: string
  file: string
  expectedTriangles: string
}

const EQUIPMENT: ModelCard[] = [
  {
    id: 'switch-1u-cisco-catalyst-c9300-48p-m',
    label: 'Cisco Catalyst C9300-48P-M',
    type: 'Switch · 1U',
    dimensions: '445 × 450 × 44 mm',
    file: '/models/switch-1u-cisco-catalyst-c9300-48p-m.glb',
    expectedTriangles: '632',
  },
  {
    id: 'server-1u-dell-poweredge-r640',
    label: 'Dell EMC PowerEdge R640',
    type: 'Server · 1U',
    dimensions: '443 × 734 × 43 mm',
    file: '/models/server-1u-dell-poweredge-r640.glb',
    expectedTriangles: '56',
  },
  {
    id: 'ups-3u-apc-smart-ups-xl-sua3000rmxl3u',
    label: 'APC Smart-UPS XL SUA3000RMXL3U',
    type: 'UPS · 3U',
    dimensions: '443 × 660 × 132 mm',
    file: '/models/ups-3u-apc-smart-ups-xl-sua3000rmxl3u.glb',
    expectedTriangles: '56',
  },
  {
    id: 'pdu-0u-vertiv-geist-rpdu-30-outlet',
    label: 'Vertiv Geist 30-Outlet rPDU',
    type: 'PDU · Vertical 0U',
    dimensions: '50 × 60 × 1700 mm',
    file: '/models/pdu-0u-vertiv-geist-rpdu-30-outlet.glb',
    expectedTriangles: '56',
  },
  {
    id: 'crac-floor-vertiv-liebert-crv',
    label: 'Vertiv Liebert CRV',
    type: 'CRAC · Floor-standing',
    dimensions: '1200 × 800 × 1800 mm',
    file: '/models/crac-floor-vertiv-liebert-crv.glb',
    expectedTriangles: '56',
  },
  {
    id: 'fire-panel-wall-generic-fm200-extinguishant-control-panel',
    label: 'FM-200 Extinguishant Control Panel',
    type: 'Fire panel · Wall-mounted',
    dimensions: '400 × 120 × 500 mm',
    file: '/models/fire-panel-wall-generic-fm200-extinguishant-control-panel.glb',
    expectedTriangles: '56',
  },
]

interface ModelProps {
  url: string
  onTriangles: (triangles: number) => void
}

function Model({ url, onTriangles }: ModelProps) {
  const gltf = useGLTF(url)

  const object = useMemo(
    () => gltf.scene.clone(true),
    [gltf.scene],
  )

  const groupRef = useRef<THREE.Group | null>(null)

  useEffect(() => {
    let triangleCount = 0

    object.traverse((child) => {
      if (!(child instanceof THREE.Mesh)) {
        return
      }

      const geometry = child.geometry

      if (geometry.index) {
        triangleCount += geometry.index.count / 3
      } else if (geometry.attributes.position) {
        triangleCount += geometry.attributes.position.count / 3
      }
    })

    onTriangles(Math.round(triangleCount))

    const group = groupRef.current

    if (!group) {
      return
    }

    group.position.set(0, 0, 0)
    group.scale.setScalar(1)

    const box = new THREE.Box3().setFromObject(group)
    const center = box.getCenter(new THREE.Vector3())
    const size = box.getSize(new THREE.Vector3())
    const maxDimension = Math.max(size.x, size.y, size.z)

    group.position.set(
      -center.x,
      -center.y,
      -center.z,
    )

    if (maxDimension > 0) {
      group.scale.setScalar(1.1 / maxDimension)
    }
  }, [object, onTriangles])

  return (
    <group ref={groupRef}>
      <primitive object={object} />
    </group>
  )
}

interface ZoomStatusProps {
  onDistanceChange: (distance: number) => void
}

function ZoomStatus({ onDistanceChange }: ZoomStatusProps) {
  const { camera } = useThree()

  useFrame(() => {
    onDistanceChange(camera.position.length())
  })

  return null
}

interface ModelViewerProps {
  card: ModelCard
  onOpen?: () => void
  fullScreen?: boolean
}

function ModelViewer({
  card,
  onOpen,
  fullScreen = false,
}: ModelViewerProps) {
  const [distance, setDistance] = useState(1.8)
  const [triangles, setTriangles] = useState<number | null>(null)

  const quality =
    distance > 1.25
      ? 'SHARP'
      : distance > 0.6
        ? 'NEAR LIMIT'
        : 'EXTREME ZOOM'

  return (
    <div
      className={`viewer ${fullScreen ? 'viewer-fullscreen' : ''}`}
      onDoubleClick={onOpen}
      title={onOpen ? 'Double-click to open full view' : undefined}
    >
      <Canvas
        camera={{
          position: [0, -1.8, 0],
          fov: 42,
          near: 0.01,
          far: 100,
          up: [0, 0, 1],
        }}
        onCreated={({ camera }) => {
          camera.up.set(0, 0, 1)
          camera.lookAt(0, 0, 0)
        }}
        gl={{
          antialias: true,
          toneMapping: THREE.ACESFilmicToneMapping,
        }}
      >
        <color attach="background" args={['#111827']} />

        <ambientLight intensity={1.2} />

        <directionalLight
          position={[3, -4, 5]}
          intensity={2.2}
        />

        <directionalLight
          position={[-3, 2, 2]}
          intensity={1.1}
        />

        <directionalLight
          position={[0, 4, -3]}
          intensity={0.8}
        />

        <Suspense
          fallback={
            <Html center>
              <div className="loading">Loading GLB...</div>
            </Html>
          }
        >
          <Model
            url={card.file}
            onTriangles={setTriangles}
          />
        </Suspense>

        <OrbitControls
          makeDefault
          enableDamping
          dampingFactor={0.08}
          minDistance={0.25}
          maxDistance={4}
          target={[0, 0, 0]}
        />

        <ZoomStatus onDistanceChange={setDistance} />
      </Canvas>

      <div
        className={`quality-badge ${
          quality === 'SHARP'
            ? 'quality-good'
            : quality === 'NEAR LIMIT'
              ? 'quality-warning'
              : 'quality-danger'
        }`}
      >
        {quality}
      </div>

      <div className="triangle-badge">
        Triangles: {triangles ?? '...'}
      </div>

      {onOpen && (
        <button
          type="button"
          className="open-view-button"
          onClick={(event) => {
            event.stopPropagation()
            onOpen()
          }}
        >
          Full view
        </button>
      )}
    </div>
  )
}

export function Gallery() {
  const [selectedCard, setSelectedCard] =
    useState<ModelCard | null>(null)

  useEffect(() => {
    if (!selectedCard) {
      return
    }

    const previousOverflow = document.body.style.overflow

    document.body.style.overflow = 'hidden'

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setSelectedCard(null)
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [selectedCard])

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <h1>MIDA-HMON — HQ Device Model Gallery</h1>

          <p>
            Drag to rotate. Use the mouse wheel to zoom.
            Double-click a model or press Full view to inspect it separately.
          </p>
        </div>

        <div className="summary">
          <strong>6</strong>
          <span>HQ models</span>
        </div>
      </header>

      <section className="gallery">
        {EQUIPMENT.map((card) => (
          <article className="card" key={card.id}>
            <div className="card-header">
              <div>
                <h2>{card.label}</h2>
                <p>{card.type}</p>
              </div>

              <span className="expected">
                Expected triangles: {card.expectedTriangles}
              </span>
            </div>

            <ModelViewer
              card={card}
              onOpen={() => setSelectedCard(card)}
            />

            <div className="metadata">
              <code>{card.id}</code>
              <span>{card.dimensions}</span>
            </div>
          </article>
        ))}
      </section>

      {selectedCard && (
        <div
          className="model-modal"
          role="dialog"
          aria-modal="true"
          aria-label={`${selectedCard.label} full view`}
        >
          <div className="model-modal-header">
            <div>
              <h2>{selectedCard.label}</h2>

              <p>
                {selectedCard.type} · {selectedCard.dimensions}
              </p>

              <code>{selectedCard.id}</code>
            </div>

            <button
              type="button"
              className="close-modal-button"
              onClick={() => setSelectedCard(null)}
            >
              ← Back to gallery
            </button>
          </div>

          <div className="model-modal-viewer">
            <ModelViewer
              card={selectedCard}
              fullScreen
            />
          </div>
        </div>
      )}
    </main>
  )
}
