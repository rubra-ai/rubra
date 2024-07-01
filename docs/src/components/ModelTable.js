import React from 'react';
import { useTable, useSortBy } from 'react-table';
import './ModelTable.css';

function ModelTable({ columns, data }) {
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        state: { sortBy }
    } = useTable(
        {
            columns,
            data,
            initialState: {
                sortBy: [
                    {
                        id: 'functionCalling', // The column to sort by
                        desc: true, // Sort in descending order
                    },
                ],
            },
        },
        useSortBy
    );

    // Function to conditionally render cell content
    const renderCellContent = (cell) => {
        // Check if the column is 'model' and if the content includes 'Rubra'
        if (cell.column.id === 'model' && cell.value.includes('Rubra')) {
            return <strong>{cell.value}</strong>;
        }
        return cell.render('Cell');
    };

    return (
        <table {...getTableProps()} className="table">
            <thead>
                {headerGroups.map(headerGroup => (
                    <tr {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map(column => (
                            <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                                {column.render('Header')}
                                {/* Add a sort direction indicator */}
                                <span>
                                    {column.isSorted
                                        ? column.isSortedDesc
                                            ? ' ↓'
                                            : ' ↑'
                                        : ''}
                                </span>
                            </th>
                        ))}
                    </tr>
                ))}
            </thead>
            <tbody {...getTableBodyProps()}>
                {rows.map(row => {
                    prepareRow(row);
                    return (
                        <tr {...row.getRowProps()}>
                            {row.cells.map(cell => (
                                <td {...cell.getCellProps()}>
                                    {renderCellContent(cell)}
                                </td>
                            ))}
                        </tr>
                    );
                })}
            </tbody>
        </table>
    );
}

export default ModelTable;
