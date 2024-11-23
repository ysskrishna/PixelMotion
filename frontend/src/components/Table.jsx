import React from 'react'
import moment from 'moment';

function isValidData(data) {
    return Array.isArray(data) && data.length > 0;
}

function getRelativeTime(isoDate) {
    return moment(isoDate).fromNow();
}

function Table({data}) {
    // Sort data by created_at in descending order
    const sortedData = [...data].sort((a, b) => 
        new Date(b.created_at) - new Date(a.created_at)
    );

    if (!isValidData(sortedData)) {
        return <></>
    }

    const handleDownload = async (videoUrl) => {
        try {
            const fileName = `video_${Date.now()}.mp4`;

            const response = await fetch(videoUrl);
            if (!response.ok) {
                throw new Error('Failed to download video');
            }

            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);


            const link = document.createElement('a');
            link.href = objectUrl;
            link.download = fileName;

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            URL.revokeObjectURL(objectUrl);
        } catch (error) {
            console.error('Error downloading video:', error);
        }
    };
    
  return (
    <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table className="table-auto w-full text-sm text-left rtl:text-right text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                    <th scope="col" className="px-6 py-3">
                        Title
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Image URL
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Status Message
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Uploaded At
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Status
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Progress
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Action
                    </th>
                </tr>
            </thead>
            <tbody>
                {
                    sortedData.map((item, index) => (
                        <tr key={index} className="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
                            <th scope="row" className="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                {item?.title}
                            </th>
                            <td className="px-6 py-3 whitespace-wrap">
                                {item?.image_url}
                            </td>
                            <td className="px-6 py-3">
                                {item?.message}
                            </td>
                            <td className="px-6 py-3">
                                {getRelativeTime(item?.created_at)}
                            </td>
                            <td className="px-6 py-3">
                                {item?.status}
                            </td>
                            <td className="px-6 py-3">
                                {item?.progress}%
                            </td>
                            <td className="px-6 py-3">
                                {item?.status === 'success' && (
                                    <button
                                        onClick={() => handleDownload(item?.video_url)}
                                        className="font-medium text-blue-600 dark:text-blue-500 hover:underline"
                                    >
                                        Download Video
                                    </button>
                                )}
                            </td>
                        </tr>
                    ))
                }
            </tbody>
        </table>
    </div>
  )
}

export default Table